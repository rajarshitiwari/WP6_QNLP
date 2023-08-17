import argparse
import json
import os
import matplotlib.pyplot as plt

def process_log_files(log_file_paths):
    k_values = []
    final_val_accs = []
    colors = []

    best_accuracy = 0.0
    best_accuracy_log = ""
    best_accuracy_k = 0
    
    # Read and process each log file
    for index, log_file_path in enumerate(log_file_paths):
        with open(log_file_path, 'r') as f:
            log_data = json.load(f)
        
        k = log_data.get("k", None)
        final_val_acc = log_data["final_val_acc"]

        for acc in final_val_acc:
            k_values.append(k)
            final_val_accs.append(acc)
            # Add a color for each experiment
            colors.append(index)

        # Keep track of the best accuracy, and the log file that produced it
        best_final_val_acc = log_data["best_final_val_acc"]
        if best_final_val_acc > best_accuracy:
            best_accuracy = best_final_val_acc
            best_accuracy_log = log_file_path
            best_accuracy_k = k
    
    return k_values, final_val_accs, colors, best_accuracy, best_accuracy_log, best_accuracy_k

def plot_accuracy_vs_k(k_values, final_val_accs, colors, best_accuracy, best_accuracy_log, best_accuracy_k):
    plt.figure(figsize=(8, 6))
    plt.scatter(k_values, final_val_accs, marker='o', c=colors, cmap='viridis')
    plt.xlabel("K value")
    plt.ylabel("Validation Accuracy")
    plt.title("Accuracy vs. K value")
    plt.grid(True)

    plt.text(0.5, 1.1, f"Overall Best Accuracy: {best_accuracy:.2f} for k={best_accuracy_k:.2f}\n(log file: {best_accuracy_log})",
             horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes)
    
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot results from log files.")
    parser.add_argument("log_files", nargs='+', help="Paths of the log files.")
    
    args = parser.parse_args()
    
    k_values, final_val_accs, colors, best_accuracy, best_accuracy_log, best_accuracy_k = process_log_files(args.log_files)
    plot_accuracy_vs_k(k_values, final_val_accs, colors, best_accuracy, best_accuracy_log, best_accuracy_k)