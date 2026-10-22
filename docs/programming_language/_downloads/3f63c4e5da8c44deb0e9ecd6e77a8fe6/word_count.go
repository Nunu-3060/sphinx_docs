// Wordcount は文章中の単語の出現回数を数え、上位の単語を表示するサンプルである。
package main

import (
	"cmp"
	"fmt"
	"regexp"
	"slices"
	"strings"
)

type wordCount struct {
	word  string
	count int
}

var wordPattern = regexp.MustCompile(`[a-z]+`)

// countWords は英単語を小文字にそろえて出現回数を数える。
func countWords(text string) map[string]int {
	counts := make(map[string]int)
	for _, w := range wordPattern.FindAllString(strings.ToLower(text), -1) {
		counts[w]++
	}
	return counts
}

// topWords は出現回数の降順、同数なら単語の昇順で上位 limit 件を返す。
func topWords(counts map[string]int, limit int) []wordCount {
	items := make([]wordCount, 0, len(counts))
	for w, c := range counts {
		items = append(items, wordCount{word: w, count: c})
	}
	slices.SortFunc(items, func(a, b wordCount) int {
		if c := cmp.Compare(b.count, a.count); c != 0 {
			return c
		}
		return cmp.Compare(a.word, b.word)
	})
	return items[:min(limit, len(items))]
}

func main() {
	text := "The quick brown fox jumps over the lazy dog. The dog sleeps."
	for _, wc := range topWords(countWords(text), 3) {
		fmt.Printf("%s: %d\n", wc.word, wc.count)
	}
}
