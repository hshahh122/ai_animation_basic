from PIL import Image, ImageDraw

# 1. Define image dimensions and background color
width, height = 200, 150
background_color = (255, 255, 255) # White

# 2. Define animation parameters
num_frames = 10 # How many frames in the animation
start_x = 0   # Starting x position of the rectangle
end_x = 100   # Ending x position of the rectangle
rect_width = 50 # Width of the rectangle
rect_height = 50 # Height of the rectangle
rect_color = (255, 0, 0) # Red

# 3. Create a list to hold all the image frames
frames = []

# 4. Loop to create each frame
for i in range(num_frames):
    # Calculate the current x position for this frame
    current_x = start_x + (end_x - start_x) * (i / (num_frames - 1))

    # Create a new blank image for this frame
    image = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(image)

    # Calculate the rectangle's bounding box for this frame
    rect_y = (height - rect_height) // 2
    draw.rectangle([current_x, rect_y, current_x + rect_width, rect_y + rect_height], fill=rect_color)

    # Add this frame to our list of frames
    frames.append(image)

# 5. Combine these frames into a GIF
if frames:
    frames[0].save("my_animation.gif", save_all=True, append_images=frames[1:], duration=100, loop=0)
    print("Animation 'my_animation.gif' created successfully!")
else:
    print("No frames were created to make a GIF.")
