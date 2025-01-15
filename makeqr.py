import os
import platform
import qrcode

def is_gui_available():
    # Check GUI

    if platform.system() == "Linux" and not os.environ.get("DISPLAY"):
        return False
    return True

def generate_qrcode_ascii(url):

    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=1, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    qr.print_ascii(invert=True)

def main():

    if is_gui_available():
        # GUI detected
        import tkinter as tk
        from tkinter import filedialog, messagebox
        from PIL import ImageTk

        def generate_qrcode_gui():
            url = url_entry.get()
            if not url:
                messagebox.showerror("Error", "Please Provide URL")
                return
            
            global qr_img
            qr_code = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
            qr_code.add_data(url)
            qr_code.make(fit=True)
            qr_img = qr_code.make_image(fill_color="black", back_color="white")

            qr_photo = ImageTk.PhotoImage(qr_img)
            qr_label.config(image=qr_photo)
            qr_label.image = qr_photo

            download_btn.config(state=tk.NORMAL)

        def download_qrcode():
            global qr_img
            if qr_img:
                file_path = filedialog.asksaveasfilename(defaultextension=".png", 
                                                         filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
                if file_path:
                    qr_img.save(file_path)
                    messagebox.showinfo("Success", "QR Code have been saved")


        root = tk.Tk()
        root.title("EasyQR")
        
        tk.Label(root, text="Type URL here to convert:").pack(pady=10)
        url_entry = tk.Entry(root, width=50)
        url_entry.pack(pady=5)

        convert_btn = tk.Button(root, text="Convert", command=generate_qrcode_gui)
        convert_btn.pack(pady=10)

        qr_label = tk.Label(root)
        qr_label.pack(pady=10)

        download_btn = tk.Button(root, text="Download QRcode", state=tk.DISABLED, command=download_qrcode)
        download_btn.pack(pady=10)

        root.mainloop()

    else:
        # GUI not found (use CLI mode instead)
        url = input("Type URL here to convert: ")
        if not url.strip():
            print("Error: Please provide valid URL")
        else:
            print("\nASCII QR Code (CLI Mode):\n")
            generate_qrcode_ascii(url)
            print("\n Do you want to save the QR Code as image? (Y/n)")
            choice = input()
            if choice.lower() == "y":
                qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
                qr.add_data(url)
                qr.make(fit=True)
                qr_img = qr.make_image(fill_color="black", back_color="white")
                qr_img.save("QRCode.png")
                print("QR Code saved as 'QRCode.png'")
            else:
                print("Cant save QR Code as image")

if __name__ == "__main__":
    main()
