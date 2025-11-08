#!/usr/bin/env python3

import os
import spacy
import json
import asyncio
import hashlib
import pickle
import signal
import numpy as np
import subprocess
from pathlib import Path
from sklearn.linear_model import LogisticRegression


def finish_affinity():
    os.system("clear")
    print("\033[0m🐧 Farewell, pengu!")
    exit(0)


signal.signal(signal.SIGINT, lambda signum, frame: finish_affinity())


class CacheManager:
    def __init__(self, cache_dir=None):
        script_dir = Path(__file__).resolve().parent
        self.cache_dir = Path(cache_dir or script_dir / ".pengu-cache")
        self.cache_dir.mkdir(exist_ok=True)
        self.vectors_path = self.cache_dir / "pengu_vectors.pkl"
        self.model_path = self.cache_dir / "pengu_model.pkl"
        self.hash_path = self.cache_dir / "pengu_hash.txt"

    def calculate_data_hash(self, data):
        data_str = json.dumps(data, sort_keys=True).encode("utf-8")
        return hashlib.md5(data_str).hexdigest()

    def save(self, vectors=None, model=None, data_hash=None):
        def save_data(path, data, binary=True):
            mode = "wb" if binary else "w"
            with open(path, mode) as f:
                if binary:
                    pickle.dump(data, f)
                else:
                    f.write(data)

        if vectors is not None:
            save_data(self.vectors_path, vectors)
        if model is not None:
            save_data(self.model_path, model)
        if data_hash is not None:
            save_data(self.hash_path, data_hash, binary=False)

    def get_cached_hash(self):
        try:
            if self.hash_path.exists():
                with open(self.hash_path, "r") as f:
                    return f.read().strip()
        except Exception:
            pass
        return None

    def _load_cached_data(self, path, current_hash=None):
        try:
            if current_hash and current_hash != self.get_cached_hash():
                return None
            if path.exists():
                with open(path, "rb") as f:
                    return pickle.load(f)
        except Exception as e:
            print(f"\n\033[1;31m~ \033[0mFailed to read cached data in {path.name}: {e}")
        return None

    def load_vectors(self, current_hash=None):
        return self._load_cached_data(self.vectors_path, current_hash)

    def load_model(self, current_hash=None):
        return self._load_cached_data(self.model_path, current_hash)


def init():
    os.system("clear")
    print(
        "\033[32m"
        + r"""
                  ⌐ `' ¬
                 ▄ ` ▌ `|┐
                 ▌  └-╛ ▐╛
               ▄██"\---╨██▄
▐██  ▄████▄      █▄████▄█   ▐██  ▄████▄     ▄▄███▄▄  ██   ██       ██
▐███▀     ███  ▄██▀    ▀██   ███▀    ▀██   ██▀     ▀███  ▐██       ██
▐██        ██  ████████████  ██▌      ██▌ ▐██       ▐██  ▐██       ██
▐███      ▄██  ███           ██▌      ██▌  ██▄     ▄███   ██▄     ███
▐██ ▀█▄▄▄███    ▀███▄▄▄▄██▀  ██▌      ██▌   ▀▀███▀▀ ▐██   ▀███▄▄██ ██
▐██                                        ▐▄▄    ▄▄██
 ▀▀                                          ▀▀▀▀▀▀▀
"""
        + "\033[0m"
    )


async def loading_animation(message):
    os.system("clear")
    try:
        chars = "|/-\\"
        i = 0
        while True:
            print(f"\r{message} {chars[i % len(chars)]}", end="", flush=True)
            i += 1
            await asyncio.sleep(0.2)
    except asyncio.CancelledError:
        pass


async def run_with_animation(message, func, *args, **kwargs):
    animation_task = asyncio.create_task(loading_animation(message))
    result = await asyncio.to_thread(func, *args, **kwargs)
    animation_task.cancel()
    return result


async def load_model():
    global nlp
    nlp = await run_with_animation(
        "Loading base model ...", spacy.load, "en_core_web_sm"
    )


async def vectorize_data(items):
    return await run_with_animation(
        "Vectorizing data ...",
        lambda texts: [doc.vector for doc in nlp.pipe(texts, batch_size=64)],
        items,
    )


async def train_model(model, X, y):
    return await run_with_animation(
        "Building model ...", lambda m, x, y: m.fit(x, y), model, X, y
    )


async def man(command):
    # Output the a shortened man page for the given command
    try:
        p1 = subprocess.Popen(
            ["man", command], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
        )
        p2 = subprocess.Popen(
            ["col", "-bx"],
            stdin=p1.stdout,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
        if p1.stdout:
            p1.stdout.close()
        output_bytes, _ = p2.communicate()
        full_text = output_bytes.decode("utf-8", errors="ignore")
    except Exception as e:
        return f"\n\033[1;31m~ \033[0mError retrieving man page: {e}"

    sections = ["NAME", "SYNOPSIS", "DESCRIPTION"]
    current_section = None
    collected_sections = {"NAME": [], "SYNOPSIS": [], "DESCRIPTION": []}

    lines = full_text.splitlines()

    for line in lines:
        if line.strip().isupper() and line.strip() and line.strip() in sections:
            current_section = line.strip()
            continue

        if current_section in ["NAME", "SYNOPSIS"]:
            if line.strip().isupper() and line.strip() in sections:
                current_section = line.strip()
            elif line.strip() != "":
                collected_sections[current_section].append(line)

        elif current_section == "DESCRIPTION":
            # Prevent further sections from displaying
            if line.strip().isupper() and line.strip() not in collected_sections:
                break

            # Some description pages have subsections
            # We must hide them to keep it all concise
            if line.startswith("   ") and not line.startswith("      "):
                break
            collected_sections["DESCRIPTION"].append(line)

    # Reveal the shortened man page
    output_parts = []
    for sec in sections:
        content = "\n".join(collected_sections[sec]).strip()
        if content:
            output_parts.append(f"\033[96m\033[1m{sec}\033[0m\n{content}")

    return "\n\n".join(output_parts)


async def main():
    await load_model()

    def load_json_file(file_path):
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return None

    script_dir = Path(__file__).resolve().parent
    training_data_path = script_dir / "pengu-training" / "data.json"
    training_data = load_json_file(training_data_path)

    if not training_data:
        print("\n\033[1;31m~ \033[0mError: Could not find training data in", training_data_path)
        return

    cache_manager = CacheManager()
    current_data_hash = cache_manager.calculate_data_hash(training_data)

    ai = cache_manager.load_model(current_data_hash)
    vectors = cache_manager.load_vectors(current_data_hash) if ai is not None else None

    if ai is not None:
        print("Using cached trained model")

    operations = list(training_data.keys())
    inputs = []
    labels = []

    for i, operation in enumerate(operations):
        inputs.extend(training_data[operation])
        labels.extend([i] * len(training_data[operation]))

    if vectors is None:
        vectors = await vectorize_data(inputs)
        cache_manager.save(vectors=vectors, data_hash=current_data_hash)

    if ai is None:
        X = np.array(vectors)
        y = np.array(labels)
        ai = LogisticRegression(n_jobs=-1, max_iter=1000)
        await train_model(ai, X, y)
        cache_manager.save(model=ai, data_hash=current_data_hash)

    while True:
        init()
        user_input = input(
            "\033[1mWelcome to pengu! Briefly describe your desired operation (^C to quit): \033[0m"
        )

        if len(user_input) < 4:
            print("\033[1;31m~ \033[0mPlease provide a more detailed description.")
            await asyncio.sleep(2)
            continue

        vector = nlp(user_input).vector.reshape(1, -1)
        predicted_index = ai.predict(vector)[0]
        operation = await man(operations[predicted_index])

        print(f"\n\033[0m{operation}\n")

        if (
            input(
                f"\033[31mpengu can make mistakes. Verify that the information is correct.\n\033[1;36m~ \033[0mDo you want to search for another operation? [Y/n]: \033[0m"
            ).lower()
            == "n"
        ):
            finish_affinity()


if __name__ == "__main__":
    asyncio.run(main())
