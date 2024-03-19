import os, modal
stub = modal.Stub(name="neuer-trainer")

image = modal.Image.debian_slim(python_version="3.10").run_commands(
    "apt-get update",
    "apt-get install -y software-properties-common",
    "apt-add-repository non-free",
    "apt-add-repository contrib",
    "pip install wandb textstat trl[peft] pandas torch datasets transformers bitsandbytes loralib",
)

@stub.function(gpu="a100", secrets=[modal.Secret.from_name("huggingface")], image=image, timeout=5000)
def train():
    from peft import LoraConfig
    from tqdm import tqdm
    import pandas as pd
    import textstat
    import torch

    tqdm.pandas()

    import wandb
    from transformers import pipeline, AutoTokenizer
    from datasets import load_dataset
    from trl import PPOTrainer, PPOConfig, AutoModelForCausalLMWithValueHead
    from torch.utils.data import Dataset
    from datasets import Dataset as HFDataset

    config = PPOConfig(
        model_name="lcrew/News-writer",
        learning_rate=1.41e-5,
        log_with="wandb",
    )

    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
    )

    wandb.login(key='90c88cae09f074c10b549b71c83b14f4ff2e22ce')
    wandb.init()

    tokenizer = AutoTokenizer.from_pretrained(config.model_name)
    tokenizer.pad_token = tokenizer.eos_token
    def tokenize(sample):
        sample["input_ids"] = tokenizer.encode(sample["input"], padding='max_length', max_length=512, truncation=True)
        return sample

    dataset = load_dataset("lcrew/data", split="train")
    dataset = dataset.map(tokenize)
    dataset.set_format(type="torch")

    print('Dataset loaded')

    if isinstance(dataset, Dataset):
        print("Your dataset is an instance of torch.utils.data.Dataset")
    elif isinstance(dataset, HFDataset):
        print("Your dataset is an instance of datasets.Dataset")
    else:
        print("Your dataset is not an instance of either torch.utils.data.Dataset or datasets.Dataset")

    model = AutoModelForCausalLMWithValueHead.from_pretrained(
        'lcrew/News-writer',
        peft_config=lora_config,
        load_in_8bit=True,
    )
    ref_model = AutoModelForCausalLMWithValueHead.from_pretrained(
        'lcrew/News-writer',
        peft_config=lora_config,
        load_in_8bit=True,
    )

    print('Models loaded')

    ppo_trainer = PPOTrainer(
        model=model,
        config=config,
        tokenizer=tokenizer,
        ref_model=ref_model,
        dataset=dataset,
    )

    generation_kwargs = {
        "min_length": -1,
        "top_k": 0.0,
        "top_p": 1.0,
        "do_sample": True,
        "pad_token_id": tokenizer.eos_token_id,
    }

    print('Training started')
    for epoch, batch in tqdm(enumerate(ppo_trainer.dataloader)):
        query_tensors = batch["input_ids"]

        #### Get response from gpt2
        response_tensors = []
        for query in query_tensors:
            gen_len = 1028
            generation_kwargs["max_new_tokens"] = gen_len
            response = ppo_trainer.generate(query, **generation_kwargs)
            response_tensors.append(response.squeeze()[-gen_len:])
        batch["response"] = [tokenizer.decode(r.squeeze()) for r in response_tensors]

        #### Compute sentiment score
        texts = [q + r for q, r in zip(batch["query"], batch["response"])]
        richtig = False
        try:
            # Nehme Variabeln aus dem Output
            titel = output
            titel = titel.split("Titel:")[1]
            titel = titel.split("Beschreibung:")[0]
            titel = titel.strip()
            beschreibung = output
            beschreibung = beschreibung.split("Beschreibung:")[1]
            beschreibung = beschreibung.split("Inhalt:")[0]
            beschreibung = beschreibung.strip()
            inhalt = output
            inhalt = inhalt.split("Inhalt:")[1]
            inhalt = inhalt.split("Keywords:")[0]
            inhalt = inhalt.strip()
            keywords = output
            keywords = keywords.split("Keywords:")[1]
            keywords = keywords.split("Kategorie:")[0]
            keywords = keywords.strip()
            bildtags = output
            bildtags = bildtags.split("Bildtag:")[1]
            bildtags = bildtags.strip()
            richtig = True
        except:
            rewards = [0.0]
        if richtig:
            text = titel + ' ' + beschreibung + ' ' + inhalt
            textlänge = int(len(text.split()))
            wiener_index = textstat.wiener_sachtextformel(text, variant=1)
            if wiener_index < 7:
                wiener_index = 15
            reward_schwierigkeit = 15 - wiener_index / 7
            reward_länge = textlänge / 700
            rewards = [reward_schwierigkeit + reward_länge / 2]

        #### Run PPO step
        stats = ppo_trainer.step(query_tensors, response_tensors, rewards)
        ppo_trainer.log_stats(stats, batch, rewards)
    model.save_pretrained("news-writer-v2", push_to_hub=True)
    tokenizer.save_pretrained("news-writer-v2", push_to_hub=True)

@stub.local_entrypoint()
def main():
    train.remote()

#if __name__ == "__main__":
#    train()