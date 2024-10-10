package main

import (
    "fmt"
    "net/http"
)

func helloWorld(w http.ResponseWriter, r *http.Request) {
    fmt.Fprint(w, "Hello World!")
}

func main() {
    http.HandleFunc("/", helloWorld)
    http.ListenAndServe(":9000", nil)
}
