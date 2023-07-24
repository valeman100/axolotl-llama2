"""Module containing the SimpleShareGPTPromptTokenizingStrategy class"""

from axolotl.prompt_tokenizers import ShareGPTPromptTokenizingStrategy
from axolotl.prompters import PromptStyle, ShareGPTPrompter


def load(tokenizer, cfg):
    return SimpleShareGPTPromptTokenizingStrategy(
        ShareGPTPrompter(PromptStyle.CHAT.value),
        tokenizer,
        cfg.train_on_inputs,
        cfg.sequence_len,
    )


def load_role(tokenizer, cfg):
    return SimpleRoleShareGPTPromptTokenizingStrategy(
        ShareGPTPrompter(PromptStyle.CHAT.value),
        tokenizer,
        cfg.train_on_inputs,
        cfg.sequence_len,
    )


def load_guanaco(tokenizer, cfg):
    return GuanacoShareGPTPromptTokenizingStrategy(
        ShareGPTPrompter(PromptStyle.CHAT.value),
        tokenizer,
        cfg.train_on_inputs,
        cfg.sequence_len,
    )


class SimpleShareGPTPromptTokenizingStrategy(ShareGPTPromptTokenizingStrategy):
    """
    basic sharegpt strategy to grab conversations from the sample row
    """

    def get_conversation_thread(self, prompt):
        return prompt["conversations"]


class SimpleRoleShareGPTPromptTokenizingStrategy(ShareGPTPromptTokenizingStrategy):
    """
    basic sharegpt strategy to grab conversations from the sample row, but uses role instead of from
    """

    def get_conversation_thread(self, prompt):
        conversations = prompt["conversations"]
        return [{"from": t["role"], "value": t["value"]} for t in conversations]


class GuanacoShareGPTPromptTokenizingStrategy(ShareGPTPromptTokenizingStrategy):
    """
    sharegpt strategy that remaps oasst data to sharegpt format
    """

    def get_conversation_thread(self, prompt):
        conversations = prompt["conversations"]
        # remap role: prompter/assistant, text: ... => from: human/gpt, value: ...
        role_map = {"prompter": "human", "assistant": "gpt"}
        return [
            {"from": role_map[t["role"]], "value": t["text"]}
            for t in conversations
        ]
