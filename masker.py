import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw


class MaskCreator:
    def __init__(self, image_path):
        self.root = tk.Tk()
        self.root.title("Mask Creator")

        # Load and resize image if necessary

        self.original_image = Image.open(image_path)
        # Maintain aspect ratio while fitting in 800x800

        max_size = 800
        ratio = min(
            max_size / self.original_image.width, max_size / self.original_image.height
        )
        new_size = (
            int(self.original_image.width * ratio),
            int(self.original_image.height * ratio),
        )
        self.image = self.original_image.resize(new_size)

        # Create mask

        self.mask = Image.new("L", self.image.size, 0)
        self.draw = ImageDraw.Draw(self.mask)

        # Create overlay

        self.overlay = Image.new("RGBA", self.image.size, (0, 0, 0, 0))
        self.overlay_draw = ImageDraw.Draw(self.overlay)

        # Convert for tkinter

        self.photo = ImageTk.PhotoImage(self.image)

        # Create canvas

        self.canvas = tk.Canvas(
            self.root, width=self.image.width, height=self.image.height
        )
        self.canvas.pack(side=tk.LEFT)
        self.canvas_image = self.canvas.create_image(
            0, 0, image=self.photo, anchor=tk.NW
        )

        # Control panel

        self.control_panel = ttk.Frame(self.root)
        self.control_panel.pack(side=tk.RIGHT, fill=tk.Y)

        # Brush size control

        ttk.Label(self.control_panel, text="Brush Size:").pack(pady=5)
        self.brush_size = tk.IntVar(value=20)
        brush_scale = ttk.Scale(
            self.control_panel,
            from_=1,
            to=50,
            variable=self.brush_size,
            orient=tk.HORIZONTAL,
        )
        brush_scale.pack(pady=5)

        # Save button

        ttk.Button(self.control_panel, text="Use Mask", command=self.save_mask).pack(
            pady=20
        )

        # Clear button

        ttk.Button(self.control_panel, text="Clear Mask", command=self.clear_mask).pack(
            pady=5
        )

        # Bind mouse events

        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<Button-1>", self.paint)

        self.result_mask = None

        # Update display

        self.update_display()

    def paint(self, event):
        x, y = event.x, event.y
        r = self.brush_size.get()
        # Draw on both mask and overlay

        self.draw.ellipse([x - r, y - r, x + r, y + r], fill=255)
        self.overlay_draw.ellipse([x - r, y - r, x + r, y + r], fill=(255, 0, 0, 128))
        self.update_display()

    def update_display(self):
        # Combine image and overlay

        composite = self.image.copy()
        composite.paste(self.overlay, (0, 0), self.overlay)
        self.photo_composite = ImageTk.PhotoImage(composite)
        self.canvas.itemconfig(self.canvas_image, image=self.photo_composite)

    def clear_mask(self):
        self.mask = Image.new("L", self.image.size, 0)
        self.draw = ImageDraw.Draw(self.mask)
        self.overlay = Image.new("RGBA", self.image.size, (0, 0, 0, 0))
        self.overlay_draw = ImageDraw.Draw(self.overlay)
        self.update_display()

    def save_mask(self):
        # Resize mask back to original image size if it was resized

        if self.mask.size != self.original_image.size:
            self.result_mask = self.mask.resize(self.original_image.size)
        else:
            self.result_mask = self.mask
        self.result_mask = np.array(self.result_mask)
        self.root.quit()

    def run(self):
        self.root.mainloop()
        return self.result_mask


def create_mask(image_path):
    """
    Opens a UI to create a mask for the given image.

    Args:
        image_path (str): Path to the image file

    Returns:
        PIL.Image: The created mask as a PIL Image in 'L' mode
        None: If the UI was closed without saving
    """
    app = MaskCreator(image_path)
    mask = app.run()
    app.root.destroy()
    return mask


if __name__ == "__main__":
    # Example usage
    import sys
    import cv2
    mask = create_mask(sys.argv[1])
    cv2.imwrite(sys.argv[2], mask)
