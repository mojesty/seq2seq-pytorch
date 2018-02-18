import torch
from torch.utils.data.dataset import Dataset
from torch.autograd import Variable

from cfg import USE_CUDA


class QADataset(Dataset):
    """
    Simple QA Dataset. Refers to torchtext.vocab for tensor creating
    """

    def __init__(self, data, vocab, max_length=30, gpu=True):
        self.vocab = vocab
        self.data = data
        self.max_length = max_length
        self.gpu = gpu

    def indexes_from_sentence(self, sentence):
        # be careful with it, as it preprocceses
        res = []
        for i, word in enumerate(sentence.split(' ')):
            if i > self.max_length:
                break
            if word == 'bos':
                res.append(0)
            elif word == 'eos':
                res.append(1)
            if word in self.vocab.stoi and self.vocab.stoi[word] < 20000 - 3:
                res.append(self.vocab.stoi[word] + 3)
            else:
                res.append(2)  # (self.vocab.stoi['unk'])
        return torch.cuda.LongTensor(res) if self.gpu else torch.LongTensor(res)

    def variable_from_sentence(self, sentence):
        indexes = self.indexes_from_sentence(sentence)
        # TODO: do we need varialbes?
        var = Variable(indexes)
        if USE_CUDA:
            var = var.cuda()
        return var

    #     def __getitem__(self, idx):
    #         return (
    #             self.variable_from_sentence(self.data[idx]['context']),
    #             self.variable_from_sentence(self.data[idx]['question'])
    #         )

    def __getitem__(self, idx):
        return (
            self.indexes_from_sentence(self.data[idx]['context']),
            self.indexes_from_sentence(self.data[idx]['question'])
        )

    def __len__(self):
        return len(self.data)