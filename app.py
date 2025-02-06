from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

algorithms = {
    "stack": "Stack",
    "queue": "Queue",
    "bubble_sort": "Bubble Sort",
    "insertion_sort": "Insertion Sort",
    "merge_sort": "Merge Sort",
    "quick_sort": "Quick Sort"
}

stack = []
queue = []


def push_stack(value):
    stack.append(value)
    return stack


def pop_stack():
    return stack.pop() if stack else None


def enqueue(value):
    queue.append(value)
    return queue


def dequeue():
    return queue.pop(0) if queue else None


def bubble_sort_steps(arr):
    steps = []
    n = len(arr)
    arr = arr[:]
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                steps.append(arr[:])
    return steps


def insertion_sort_steps(arr):
    steps = []
    arr = arr[:]
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
            steps.append(arr[:])
        arr[j + 1] = key
        steps.append(arr[:])
    return steps


def merge_sort_steps(arr):
    steps = []

    def merge_sort_inner(arr):
        if len(arr) > 1:
            mid = len(arr) // 2
            left_half = arr[:mid]
            right_half = arr[mid:]
            merge_sort_inner(left_half)
            merge_sort_inner(right_half)
            i = j = k = 0
            while i < len(left_half) and j < len(right_half):
                if left_half[i] < right_half[j]:
                    arr[k] = left_half[i]
                    i += 1
                else:
                    arr[k] = right_half[j]
                    j += 1
                k += 1
                steps.append(arr[:])
            while i < len(left_half):
                arr[k] = left_half[i]
                i += 1
                k += 1
                steps.append(arr[:])
            while j < len(right_half):
                arr[k] = right_half[j]
                j += 1
                k += 1
                steps.append(arr[:])

    merge_sort_inner(arr[:])
    return steps


def quick_sort_steps(arr):
    steps = []

    def quick_sort_inner(arr):
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        sorted_arr = quick_sort_inner(left) + middle + quick_sort_inner(right)
        steps.append(sorted_arr[:])
        return sorted_arr

    quick_sort_inner(arr[:])
    return steps


@app.route('/')
def index():
    return render_template("index.html", algorithms=algorithms)


@app.route('/visualize/<algorithm>')
def visualize(algorithm):
    if algorithm not in algorithms:
        return "Algorithm not found", 404
    return render_template("visualize.html", algorithm=algorithm)


@app.route('/sort', methods=['POST'])
def sort():
    data = request.json
    algorithm = data.get("algorithm")
    values = data.get("values")
    if not values:
        return jsonify(error="No values provided"), 400
    arr = list(map(int, values.split()))

    if algorithm == "bubble_sort":
        steps = bubble_sort_steps(arr)
    elif algorithm == "insertion_sort":
        steps = insertion_sort_steps(arr)
    elif algorithm == "merge_sort":
        steps = merge_sort_steps(arr)
    elif algorithm == "quick_sort":
        steps = quick_sort_steps(arr)
    else:
        return jsonify(error="Invalid algorithm"), 400

    return jsonify(original=values, steps=steps, sorted=steps[-1] if steps else arr)


@app.route('/stack', methods=['POST'])
def stack_operations():
    data = request.json
    operation = data.get("operation")
    value = data.get("value")
    if operation == "push":
        push_stack(value)
    elif operation == "pop":
        pop_stack()
    return jsonify(stack=stack)


@app.route('/queue', methods=['POST'])
def queue_operations():
    data = request.json
    operation = data.get("operation")
    value = data.get("value")
    if operation == "enqueue":
        enqueue(value)
    elif operation == "dequeue":
        dequeue()
    return jsonify(queue=queue)


if __name__ == "__main__":
    app.run(debug=True)
