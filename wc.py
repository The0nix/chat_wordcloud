import re
from collections import Counter
from pathlib import Path
from typing import Union, Optional

import numpy as np
import nltk
from wordcloud import WordCloud
from PIL import Image
from nltk.corpus import stopwords

nltk.download('stopwords')


STOPWORDS_SET = set(stopwords.words('russian') + ['всё', 'её', 'ещё', 'чём', 'неё', 'это'])

PUNCTUATION = '.,!?-—–_[]{}()@#$%^"\'\\/+><'
PUNCTUATION_STOPWORDS = list(PUNCTUATION) + ['...'] + list('0123456789')
PUNCTUATION_STOPWORDS.remove(')')
PUNCTUATION_STOPWORDS.remove('(')
PUNCTUATION_STOPWORDS.remove('+')

WORD_RE = re.compile(r'[A-Za-zА-Яа-яЁё0-9-]+')
PUNCTUATION_RE = re.compile(f'[{re.escape(PUNCTUATION)}]+')
MINUS_RE = re.compile(r"(?<!\w)-|-(?!\w)")


def build_word_cloud(
        messages: list[str],
        mask_path: Union[Path, str, bytes],
        size: tuple[int, int] = (2000, 2000),
        additional_stopwords: Optional[list[str]] = None,
    ) -> WordCloud:
    additional_stopwords = additional_stopwords or []

    stopwords_set = set(additional_stopwords) | STOPWORDS_SET

    words = [word.lower() for message in messages for word in WORD_RE.findall(message)]
    words = [word for word in words if word not in stopwords_set]
    words = [word for word in words if word not in PUNCTUATION_STOPWORDS]
    punctwords = [word.lower() for message in messages for word in PUNCTUATION_RE.findall(message)]
    punctwords = [word for word in punctwords if word not in stopwords_set]
    punctwords = [word for word in punctwords if word not in PUNCTUATION_STOPWORDS]
    minuses = [m for m in messages if m == '-']
    counter = Counter(words + punctwords + minuses)

    mask_image = Image.open(mask_path).convert('RGBA')
    mask_image = mask_image.resize(size)
    mask = np.array(mask_image)
    wc = WordCloud(background_color="white", max_words=2000, mask=mask)
    wc.generate_from_frequencies(counter)

    return wc


