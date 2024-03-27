import numpy as np
import matplotlib.pyplot as plt
from Classes import *
from scipy.interpolate import interp1d
import imageio


image_3 = Image("images.jpeg") # insert the image path 
image_3.convert_to_grayscale()
processor = ImageProcessor()
magnitude = processor.get_edges(image_3, "sobel_3x3", filter_flag=False) # retruns data not image object 

image_4 = Image(image_data = magnitude)
processor.apply_filter(image_4, "gaussian", sigma = 20)




def resample_contour(contour, num_points):
    # Calculate the cumulative distance along the contour
    cumulative_distance = np.cumsum(np.sqrt(np.sum(np.diff(contour, axis=0)**2, axis=1)))
    
    # Normalize the cumulative distance to range [0, 1]
    normalized_distance = cumulative_distance / cumulative_distance[-1]
    
    # Ensure that normalized_distance has the same length as contour
    normalized_distance = np.linspace(0, 1, len(contour))
    
    # Create an interpolation function for each coordinate
    interp_func_x = interp1d(normalized_distance, contour[:, 0], kind='cubic')
    interp_func_y = interp1d(normalized_distance, contour[:, 1], kind='cubic')
    
    # Generate evenly spaced samples along the contour
    t = np.linspace(0, 1, num_points)
    resampled_contour = np.column_stack((interp_func_x(t), interp_func_y(t)))
    
    return resampled_contour

plt.ion()
def onmove(event):
    global drawing, contour # reference the global variables
    if drawing and event.inaxes == ax:
        x, y = int(round(event.xdata)), int(round(event.ydata))
        contour = np.vstack((contour, [x, y])) 
        if len(contour) > 1:
            ax.plot([contour[-2, 0], x], [contour[-2, 1], y], 'r-') 
        plt.draw()

def onpress(event):
    global drawing, contour # declare them as global variables
    if event.button == 1 and event.inaxes == ax:
        drawing = True
        x, y = event.xdata, event.ydata
        x, y = int(round(x)), int(round(y))  
        contour = np.array([[x, y]])

def onrelease(event):
    global drawing, contour
    if event.button == 1:
        drawing = False
        if len(contour) > 0:
            # Resample the collected contour
            num_points = len(contour) // 2   # Change this number as needed
            resampled_contour = resample_contour(contour, num_points)

            ax.plot(resampled_contour[:, 0], resampled_contour[:, 1], 'ro')
            
            contour = np.array(resampled_contour, dtype=int)


image = image_3.original_img
fig, ax = plt.subplots()
ax.imshow(image, cmap='gray')
ax.axis('off')
plt.tight_layout()

contour = np.array([])
drawing = False

# Connect event handlers
cid1 = fig.canvas.mpl_connect('motion_notify_event', onmove)
cid2 = fig.canvas.mpl_connect('button_press_event', onpress)
cid3 = fig.canvas.mpl_connect('button_release_event', onrelease)


input("Press Enter when done...")

print(len(contour))
print(contour)
print(image_3.original_img.shape)


def compute_internal_energy(contour, control_idx, neighbour_pos):
    prev_idx = control_idx - 1 if control_idx > 0 else len(contour) - 1
    next_idx = control_idx + 1 if control_idx < len(contour) - 1 else 0
    # if the control_pos = neighbour_pos, then i'm compute the internal energy of the control point. (how it vote to the overall energy in the contour) 

    # finite difference way of computation.
    E_elastic = abs(contour[next_idx, 0] - neighbour_pos[0]) + abs(contour[next_idx, 1] - neighbour_pos[1])
    E_smooth = abs(contour[next_idx, 0] - 2 * neighbour_pos[0] + contour[prev_idx, 0]) + abs(contour[next_idx, 1] - 2 * neighbour_pos[1] + contour[prev_idx, 1])

    internal_energy = (E_elastic, E_smooth)

    return internal_energy

def get_neighbours_with_indices(image_gradient, loc, window_size):
    margin = window_size // 2
    i = loc[0] - margin
    j = loc[1] - margin
    i_start = max(0, i)
    j_start = max(0, j)
    i_end_candidate = i_start + window_size
    i_end = np.min((image_gradient.shape[0], i_end_candidate))

    j_end_candidate = j_start + window_size
    j_end = np.min((image_gradient.shape[1], j_end_candidate))


    neighbour_grad = image_gradient[i_start:i_end, j_start:j_end]

    neighbour_indices = np.zeros_like(neighbour_grad, dtype=tuple)

    for x in range(neighbour_indices.shape[0]):
        for y in range(neighbour_indices.shape[1]):
            neighbour_indices[x, y] = (i_start + x, j_start + y)

    return neighbour_grad, neighbour_indices


def update_contour(image_gradient ,contour, window_size ,alpha = 1, beta = 0.5 ,gama = 1):

    for control_idx, control_point in enumerate(contour):
        neighbour_grad, neighbour_indices =  get_neighbours_with_indices(image_gradient, control_point, window_size)
        external_energy_neighbours = neighbour_grad * gama * -1 
        internal_energy_neighbour = np.zeros_like(neighbour_grad)
        for row in range(neighbour_indices.shape[0]):
            for col in range(neighbour_indices.shape[1]):
                E_elastic, E_smooth = compute_internal_energy(contour,control_idx,neighbour_indices[row,col])
                internal_energy_neighbour[row, col] = alpha * E_elastic + beta * E_smooth


        overall_energy_neighbours =   external_energy_neighbours + internal_energy_neighbour 
        min_energy = np.argmin(overall_energy_neighbours)

        i, j = np.unravel_index(min_energy, overall_energy_neighbours.shape)

        i_actual, j_actual = neighbour_indices[i,j]

        contour[control_idx] = [i_actual, j_actual]
    return  contour 


        
window_size = 3

ALPHA = 0.5
BETA = 1
GAMA = 0.2

frames = []
num_iterations = 20 

for _ in range(num_iterations):
    print("update")

    contour = update_contour(image_4.original_img, contour, window_size, alpha=ALPHA, beta=BETA ,gama = GAMA)

    # Clear and redraw the plot
    ax.clear()
    ax.imshow(image_3.original_img, cmap='gray')
    ax.plot(contour[:, 0], contour[:, 1], 'ro-')

    # # Save the current frame
    fig.canvas.draw()
    frame = np.array(fig.canvas.renderer.buffer_rgba())
    frames.append(frame)

imageio.mimsave('snake_animation.gif', frames, fps=10)


fig_2, ax_2 = plt.subplots()
ax_2.imshow(image_3.original_img, cmap='gray')
ax_2.plot(contour[:, 0], contour[:, 1], 'ro')
ax.axis('off')
plt.tight_layout()
