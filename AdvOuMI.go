package main

import (
    "fmt"
    "time"
)

type Counter struct {
    Value int
}

func increment(c *Counter) {
    for i := 0; i < 1000; i++ {
        c.Value++ // Race condition!  This is NOT thread-safe.
        time.Sleep(time.Microsecond) // Simulate some work
    }
}

func main() {
    counter := Counter{Value: 0}

    go increment(&counter)
    go increment(&counter)

    time.Sleep(1*time.Second) // Wait for goroutines to finish
    fmt.Println("Final value:", counter.Value) // The result will be unpredictable!
}