from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from PIL import Image, ImageDraw, ImageFont # Added ImageFont
import math # Added math

app = Flask(__name__)

# Configure a directory to serve static files (like our GIF)
app.config['UPLOAD_FOLDER'] = 'static'
# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route('/')
def index():
    # This is the main page of our website
    # We'll create an HTML file named 'index.html' later
    return render_template('index.html')

@app.route('/animation/<filename>')
def serve_animation(filename):
    # This route will serve files from our 'static' directory
    # This is how the browser will access the GIF file
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except FileNotFoundError:
        # Handle case where the GIF hasn't been generated yet
        # You might want to serve a default image or an empty one
        # For now, let's just return a simple message (won't display an image)
        # print(f"File not found: {filename} in {app.config['UPLOAD_FOLDER']}")
        # A better approach might be to serve a default static image like a placeholder
        # return send_from_directory(app.config['UPLOAD_FOLDER'], 'placeholder.gif') # If you create one
        return "Animation not found. Generate one first!" # Simple text response


@app.route('/generate_animation', methods=['POST'])
def generate_animation():
    # Check if the request method is POST
    if request.method == 'POST':
        # Get the text entered by the user from the form
        user_text = request.form.get('user_text') # 'user_text' matches the 'name' attribute in the HTML input

        if user_text: # Check if the user actually entered text
            print(f"Received text: {user_text}") # Print the received text (for debugging)

            # --- Animation Generation Logic ---
            # This is where we'll put the code similar to image_test.py

            # 1. Define image dimensions and background color
            width, height = 300, 100 # Slightly larger for text
            background_color = (200, 200, 255) # Light blue background

            # 2. Define animation parameters
            num_frames = 15 # More frames for smoother text animation
            text_color = (0, 0, 0) # Black text

            # 3. Create a list to hold all the image frames
            frames = []

            # Simple example: Make the text slide in
            # We'll calculate the text width to center it
            font = None
            text_width = 0
            text_height = 0

            try:
                # Use a basic font (Pillow needs a font file)
                # You might not have this font, so we'll handle the error
                font_path = os.path.join(os.path.dirname(__file__), "arial.ttf") # Try to find arial.ttf in the same directory
                if not os.path.exists(font_path):
                     # Fallback if arial.ttf is not found
                     font = ImageFont.load_default()
                     print("Warning: arial.ttf not found. Using default font.")
                else:
                     font = ImageFont.truetype(font_path, 30) # Font size 30
                     print(f"Using font: {font_path}")


                # Calculate text size (requires a font)
                # Use textbbox for more accurate size with current Pillow versions
                try:
                     # Create a temporary draw object to measure text
                     temp_draw = ImageDraw.Draw(Image.new('RGB', (1, 1)))
                     left, top, right, bottom = temp_draw.textbbox((0, 0), user_text, font=font)
                     text_width = right - left
                     text_height = bottom - top
                     # print(f"Text size (bbox): {text_width}x{text_height}")
                except AttributeError:
                     # Fallback for older Pillow versions without textbbox
                     text_width, text_height = ImageDraw.Draw(Image.new('RGB', (1, 1))).textsize(user_text, font=font)
                     print("Warning: Using deprecated textsize. Consider updating Pillow.")
                     # print(f"Text size (textsize): {text_width}x{text_height}")


            except ImportError:
                # Fallback if Pillow doesn't support ImageFont (unlikely with recent installs)
                font = None
                text_width = len(user_text) * 10 # Estimate width
                text_height = 20 # Estimate height
                print("Warning: ImageFont not available. Text positioning may be inaccurate.")
            except Exception as e:
                print(f"An error occurred while loading font or calculating text size: {e}")
                font = None
                text_width = len(user_text) * 10 # Estimate width
                text_height = 20 # Estimate height
                print("Falling back to estimated text size.")



            # Starting position (off-screen to the right)
            start_x = width
            # Ending position (centered horizontally)
            end_x = (width - text_width) // 2
            # Vertical position (centered)
            text_y = (height - text_height) // 2


            # Ensure text doesn't go off the left edge if it's very wide
            if end_x < 0:
                end_x = 0 # Start from the left edge if text is wider than image


            # 4. Loop to create each frame
            for i in range(num_frames):
                # Calculate the current x position for this frame
                # We'll ease the movement slightly
                progress = i / (num_frames - 1)
                # Simple easing function (smooth start and end)
                eased_progress = 0.5 - 0.5 * math.cos(progress * math.pi)

                current_x = start_x + (end_x - start_x) * eased_progress


                # Create a new blank image for this frame
                image = Image.new('RGB', (width, height), background_color)
                draw = ImageDraw.Draw(image)

                # Draw the text
                if font:
                     draw.text((current_x, text_y), user_text, fill=text_color, font=font)
                else:
                     # Draw text without font (basic fallback)
                     draw.text((current_x, text_y), user_text, fill=text_color)


                # Add this frame to our list of frames
                frames.append(image)

            # 5. Combine these frames into a GIF
            gif_filename = "my_animation.gif" # We'll overwrite the default one for now
            gif_path = os.path.join(app.config['UPLOAD_FOLDER'], gif_filename)

            try:
                if frames:
                    frames[0].save(gif_path, save_all=True, append_images=frames[1:], duration=75, loop=0) # Slightly faster duration
                    print(f"Animation '{gif_filename}' created successfully at {gif_path}!")
                else:
                    print("No frames were created to make a GIF.")
            except Exception as e:
                print(f"Error saving GIF: {e}")


            # --- End Animation Generation Logic ---

            # After generating the GIF, redirect the user back to the main page
            # The browser will then load the updated GIF in the img tag
            return redirect(url_for('index')) # 'index' is the name of our route function for the main page

        else:
            # If no text was entered, maybe redirect back or show an error
            print("No text received from the form.")
            # Optionally, add a message to the template indicating no text was entered
            return redirect(url_for('index')) # Redirect back to the main page

    # If the request method is not POST (e.g., GET), just redirect to the index
    return redirect(url_for('index'))


if __name__ == '__main__':
    # This runs the Flask development server
    # debug=True allows for automatic reloading when you make changes
    # host='0.0.0.0' makes the server accessible externally (useful for testing hosting)
    # Change back to host='127.0.0.1' for local-only access
    app.run(debug=True, host='127.0.0.1', port=5000) # Explicitly set host and port
