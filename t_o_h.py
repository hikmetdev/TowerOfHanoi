import tkinter as tk
from tkinter import messagebox

class TowerOfHanoiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tower of Hanoi")
        
        # Pencereyi ekranın ortasında konumlandır
        self.root.geometry("600x400")
        self.center_window()
        
        # Ana paneli oluştur
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas ve butonlar için iki ayrı frame oluştur
        self.canvas_frame = tk.Frame(self.main_frame)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.canvas = tk.Canvas(self.canvas_frame, width=600, height=300, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.disk_count = 3
        self.steps = 0
        self.towers = {'A': [], 'B': [], 'C': []}
        self.selected_disk = None
        self.disk_colors = ["red", "green", "blue", "yellow", "purple", "orange", "pink", "cyan"]
        self.create_widgets()
        self.reset_game()

    def center_window(self):
        # Pencerenin ekranın ortasında olması için hesaplama yapar
        window_width = 600
        window_height = 400
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')

    def create_widgets(self):
        self.decrease_button = tk.Button(self.button_frame, text="Decrease Disks", command=self.decrease_disks)
        self.decrease_button.grid(row=0, column=0, padx=5, pady=5, sticky='w')

        self.increase_button = tk.Button(self.button_frame, text="Increase Disks", command=self.increase_disks)
        self.increase_button.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        self.reset_button = tk.Button(self.button_frame, text="Reset", command=self.reset_game)
        self.reset_button.grid(row=0, column=2, padx=5, pady=5, sticky='w')

        self.solve_button = tk.Button(self.button_frame, text="Solve", command=self.solve_game)
        self.solve_button.grid(row=0, column=3, padx=5, pady=5, sticky='w')

        self.step_label = tk.Label(self.button_frame, text=f"Steps: {self.steps}")
        self.step_label.grid(row=0, column=4, padx=5, pady=5, sticky='w')

        # Butonların sütun genişliklerini ayarla
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)
        self.button_frame.grid_columnconfigure(2, weight=1)
        self.button_frame.grid_columnconfigure(3, weight=1)
        self.button_frame.grid_columnconfigure(4, weight=1)

    def reset_game(self):
        self.steps = 0
        self.update_steps()
        self.towers = {'A': list(range(self.disk_count, 0, -1)), 'B': [], 'C': []}
        self.draw_towers()

    def draw_towers(self):
        self.canvas.delete("all")
        # Çubukları yukarı taşımak için konumlarını ayarla
        self.canvas.create_rectangle(90, 100, 110, 300, fill="black")
        self.canvas.create_rectangle(290, 100, 310, 300, fill="black")
        self.canvas.create_rectangle(490, 100, 510, 300, fill="black")
        self.update_towers()

    def update_towers(self):
        self.canvas.delete("disk")
        for tower in ['A', 'B', 'C']:
            x = 100 if tower == 'A' else 300 if tower == 'B' else 500
            for i, disk in enumerate(self.towers[tower]):
                self.draw_disk(x, 300 - 20 * i, disk, tower)

    def draw_disk(self, x, y, disk, tower):
        color = self.disk_colors[disk - 1]
        disk_id = self.canvas.create_oval(x - 15 * disk, y - 15, x + 15 * disk, y + 15, fill=color, outline="black", tags=("disk", f"{tower}", f"{disk}"))
        self.canvas.tag_bind(disk_id, "<ButtonPress-1>", self.on_disk_press)
        self.canvas.tag_bind(disk_id, "<B1-Motion>", self.on_disk_motion)
        self.canvas.tag_bind(disk_id, "<ButtonRelease-1>", self.on_disk_release)

    def on_disk_press(self, event):
        disk_tags = self.canvas.gettags(event.widget.find_withtag("current")[0])
        self.selected_disk = (event.widget.find_withtag("current")[0], disk_tags[1])
        self.start_x = event.x
        self.start_y = event.y

    def on_disk_motion(self, event):
        if self.selected_disk:
            dx = event.x - self.start_x
            dy = event.y - self.start_y
            self.canvas.move(self.selected_disk[0], dx, dy)
            self.start_x = event.x
            self.start_y = event.y

    def on_disk_release(self, event):
        if self.selected_disk:
            x = event.x
            y = event.y
            target_tower = None
            if 50 <= x <= 150:
                target_tower = 'A'
            elif 250 <= x <= 350:
                target_tower = 'B'
            elif 450 <= x <= 550:
                target_tower = 'C'

            if target_tower:
                source_tower = self.selected_disk[1]
                disk_num = int(self.canvas.gettags(self.selected_disk[0])[2])
                if self.is_valid_move(disk_num, source_tower, target_tower):
                    self.towers[source_tower].remove(disk_num)
                    self.towers[target_tower].append(disk_num)
                    self.update_towers()
                    self.steps += 1
                    self.update_steps()
                    self.check_game_finished()
                else:
                    self.reset_disk_position()
            else:
                self.reset_disk_position()
            self.selected_disk = None

    def is_valid_move(self, disk_num, source_tower, target_tower):
        if not self.towers[target_tower] or disk_num < self.towers[target_tower][-1]:
            return True
        return False

    def reset_disk_position(self):
        self.update_towers()

    def update_steps(self):
        self.step_label.config(text=f"Steps: {self.steps}")

    def decrease_disks(self):
        if self.disk_count > 3:
            self.disk_count -= 1
            self.reset_game()

    def increase_disks(self):
        if self.disk_count < 8:
            self.disk_count += 1
            self.reset_game()

    def solve_game(self):
        self.reset_game()
        self.move_tower(self.disk_count, 'A', 'C', 'B')

    def move_tower(self, n, source, target, auxiliary):
        if n > 0:
            self.move_tower(n - 1, source, auxiliary, target)
            self.move_disk(source, target)
            self.root.update()
            self.root.after(500)
            self.move_tower(n - 1, auxiliary, target, source)

    def move_disk(self, source, target):
        disk = self.towers[source].pop()
        self.towers[target].append(disk)
        self.update_towers()
        self.steps += 1
        self.update_steps()
        self.check_game_finished()

    def check_game_finished(self):
        if len(self.towers['C']) == self.disk_count:
            messagebox.showinfo("Game Over", "Congratulations! You've solved the Tower of Hanoi.")
            self.reset_game()

if __name__ == "__main__":
    root = tk.Tk()
    app = TowerOfHanoiApp(root)
    root.mainloop()
