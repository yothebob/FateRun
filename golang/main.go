package main

import (
	"fmt"
	"math/rand/v2"
	"time"
)

func map_list_to_char(lst []int) string {
	res_string := ""
	for _, e := range lst {
		switch {
		case e < 5:
			res_string = res_string + "_"
		case e < 10:
			res_string = res_string + "."
		case e < 20:
			res_string = res_string + "*"
		case e < 30:
			res_string = res_string + "+"
		case e < 40:
			res_string = res_string + "%"
		default:
			res_string = res_string + "#"
		}

	}
	return res_string
}

func abs(x int) int {
	if x < 0 {
		x = -x
	}
	return x
}

func randRange(min, max int) int {
	if max == 0 {
		max = 1
	}
	return rand.IntN(max-min) + min
}

func main() {
	start := time.Now()
	array_len := 50
	variance := randRange(1, 10)
	test_array := make([][]int, array_len/2)
	for i := 0; i < array_len/2; i++ {
		test_array[i] = make([]int, array_len)
		for j := 0; j < (array_len); j++ {
			val := randRange(0,
				abs((int(array_len^2) - abs(int(i^2-(array_len-randRange((j-variance), (j+variance))))+abs(j^2-(array_len-i))))))
			test_array[i][j] = val
		}
	}

	for _, e := range test_array {
		fmt.Println(map_list_to_char(e))
	}
	t := time.Now()
	elapsed := t.Sub(start)
	fmt.Println(elapsed)
}
