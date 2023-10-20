import sys
import matplotlib.pyplot as plt
import os
import numpy as np

if __name__ == '__main__':
    if len(sys.argv) > 1:
        datetime_str = sys.argv[1]
        print(f"Received datetime: {datetime_str}")
    else:
        print("No datetime argument provided!")
    
    LOSS_PATH = f"../training/{datetime_str}/loss_data/"
    
    tr_filename = f"trainloss_{datetime_str}.npy"
    v_filename = f"valloss_{datetime_str}.npy"
    
    training_losses = np.load(LOSS_PATH + tr_filename)
    validation_losses = np.load(LOSS_PATH + v_filename)
    
    num_epochs = len(training_losses)
    print(num_epochs)
    epochs = range(1, num_epochs + 1)
    
    plt.figure(figsize=(10, 6))
    plt.plot(epochs, training_losses, '-o', label='Training Loss', color='blue')
    plt.plot(epochs, validation_losses, '-o', label='Validation Loss', color='red')
    plt.title('Training and Validation Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True)

    PLOT_PATH = f"../training/{datetime_str}/plots/"
    
    if not os.path.exists(PLOT_PATH):
        os.makedirs(PLOT_PATH)
             
    output_filename = f"loss_plot_{datetime_str}.png"
    plt.savefig(PLOT_PATH + output_filename, dpi=300)
    print(f"Plot saved as {output_filename}")