"""Hand-authored vectors: a math exercise, not an embedding or database benchmark."""
import json
import math


def cosine(left, right):
    if len(left) != len(right) or not left:
        raise ValueError('Vectors must have the same positive dimension')
    if not all(math.isfinite(x) for x in [*left, *right]):
        raise ValueError('Components must be finite')
    norm_left = math.sqrt(sum(x*x for x in left))
    norm_right = math.sqrt(sum(x*x for x in right))
    if not norm_left or not norm_right:
        raise ValueError('Zero vectors have no cosine direction')
    return sum(a*b for a, b in zip(left, right)) / (norm_left*norm_right)


def demo():
    records = [
        {'id': 1, 'language': 'fa', 'vector': [1.0, 0.0, 0.0]},
        {'id': 2, 'language': 'fa', 'vector': [0.8, 0.6, 0.0]},
        {'id': 3, 'language': 'en', 'vector': [0.0, 1.0, 0.0]},
    ]
    query = [1.0, 0.0, 0.0]
    results = sorted(
        [{'id': row['id'], 'similarity': round(cosine(query, row['vector']), 6)}
         for row in records if row['language'] == 'fa'],
        key=lambda row: (-row['similarity'], row['id']),
    )
    assert results == [{'id': 1, 'similarity': 1.0}, {'id': 2, 'similarity': 0.8}]
    assert math.isclose(cosine([2, 0, 0], query), 1.0)
    for left, right in [([0, 0], [1, 0]), ([1], [1, 0])]:
        try:
            cosine(left, right)
        except ValueError:
            pass
        else:
            raise AssertionError('Expected invalid input to be rejected')
    return results


if __name__ == '__main__':
    print(json.dumps(demo(), indent=2))
