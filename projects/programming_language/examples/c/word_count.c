/* 文章中の単語の出現回数を数え、上位の単語を表示するサンプル */
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_WORDS 64
#define MAX_WORD_LEN 32

typedef struct {
    char word[MAX_WORD_LEN];
    int count;
} WordCount;

/* 単語を表に追加する。既に登録済みなら出現回数を 1 増やす。
   word の長さは MAX_WORD_LEN - 1 以下であること */
static void add_word(WordCount *table, size_t *size, const char *word) {
    for (size_t i = 0; i < *size; i++) {
        if (strcmp(table[i].word, word) == 0) {
            table[i].count++;
            return;
        }
    }
    if (*size < MAX_WORDS) {
        memcpy(table[*size].word, word, strlen(word) + 1);
        table[*size].count = 1;
        (*size)++;
    }
}

/* 出現回数の降順、同数なら単語の昇順に並べるための比較関数 */
static int compare_word_count(const void *a, const void *b) {
    const WordCount *x = a;
    const WordCount *y = b;
    if (x->count != y->count) {
        return (x->count < y->count) - (x->count > y->count);
    }
    return strcmp(x->word, y->word);
}

int main(void) {
    const char *text = "The quick brown fox jumps over the lazy dog. The dog sleeps.";
    WordCount table[MAX_WORDS];
    size_t size = 0;
    char word[MAX_WORD_LEN];
    size_t len = 0;

    /* 英字の並びを 1 単語として切り出し、小文字にそろえて登録する */
    for (const char *p = text;; p++) {
        if (isalpha((unsigned char)*p)) {
            if (len < MAX_WORD_LEN - 1) {
                word[len++] = (char)tolower((unsigned char)*p);
            }
            continue;
        }
        if (len > 0) {
            word[len] = '\0';
            add_word(table, &size, word);
            len = 0;
        }
        if (*p == '\0') {
            break;
        }
    }

    qsort(table, size, sizeof table[0], compare_word_count);
    for (size_t i = 0; i < size && i < 3; i++) {
        printf("%s: %d\n", table[i].word, table[i].count);
    }
    return EXIT_SUCCESS;
}
