"""
Profile Manager GUI Module
GUI for managing configuration profiles.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional, Callable
import json


class ProfileManagerWindow:
    """
    A window for managing configuration profiles.
    """
    
    def __init__(self, parent, profile_manager, config_manager, 
                 on_profile_change: Optional[Callable] = None):
        """
        Initialize the profile manager window.
        
        Args:
            parent: Parent window
            profile_manager: ProfileManager instance
            config_manager: ConfigManager instance
            on_profile_change: Callback when active profile changes
        """
        self.parent = parent
        self.profile_manager = profile_manager
        self.config_manager = config_manager
        self.on_profile_change = on_profile_change
        
        # Create window
        self.window = tk.Toplevel(parent)
        self.window.title("Profile Manager")
        self.window.geometry("700x500")
        self.window.resizable(True, True)
        
        # Create UI
        self._create_ui()
        
        # Load profiles
        self._refresh_profile_list()
    
    def _create_ui(self):
        """Create the UI components."""
        # Main container
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Profile Manager", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Profile list frame
        list_frame = ttk.LabelFrame(main_frame, text="Profiles", padding="10")
        list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), 
                       padx=(0, 5))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Treeview for profiles
        columns = ('name', 'keys', 'modified')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='tree headings',
                                 selectmode='browse')
        
        self.tree.heading('#0', text='Active')
        self.tree.heading('name', text='Name')
        self.tree.heading('keys', text='Keys')
        self.tree.heading('modified', text='Modified')
        
        self.tree.column('#0', width=60, stretch=False)
        self.tree.column('name', width=150)
        self.tree.column('keys', width=150)
        self.tree.column('modified', width=120)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, 
                                 command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self._on_profile_selected)
        self.tree.bind('<Double-1>', self._on_profile_double_click)
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=1, column=1, sticky=(tk.N, tk.W), padx=(5, 0))
        
        button_configs = [
            ("New Profile", self._create_profile),
            ("Activate", self._activate_profile),
            ("Edit", self._edit_profile),
            ("Duplicate", self._duplicate_profile),
            ("Delete", self._delete_profile),
            ("", None),  # Separator
            ("Import", self._import_profile),
            ("Export", self._export_profile),
            ("", None),  # Separator
            ("Refresh", self._refresh_profile_list),
        ]
        
        for i, (text, command) in enumerate(button_configs):
            if text == "":
                ttk.Separator(buttons_frame, orient=tk.HORIZONTAL).grid(
                    row=i, column=0, sticky=(tk.W, tk.E), pady=5)
            else:
                btn = ttk.Button(buttons_frame, text=text, command=command,
                               width=15)
                btn.grid(row=i, column=0, pady=2, sticky=tk.W)
        
        # Profile details frame
        details_frame = ttk.LabelFrame(main_frame, text="Profile Details", 
                                      padding="10")
        details_frame.grid(row=2, column=0, columnspan=2, 
                          sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.details_text = tk.Text(details_frame, height=8, width=60,
                                    wrap=tk.WORD, state=tk.DISABLED)
        self.details_text.pack(fill=tk.BOTH, expand=True)
        
        # Button bar at bottom
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.grid(row=3, column=0, columnspan=2, 
                         sticky=(tk.E), pady=(10, 0))
        
        ttk.Button(bottom_frame, text="Close", 
                  command=self.window.destroy).pack(side=tk.RIGHT)
    
    def _refresh_profile_list(self):
        """Refresh the profile list."""
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get profiles
        profiles = self.profile_manager.list_profiles()
        active_profile = self.profile_manager.get_active_profile()
        active_id = active_profile.id if active_profile else None
        
        # Add profiles to tree
        for profile in profiles:
            is_active = "✓" if profile.id == active_id else ""
            keys = ", ".join(profile.config.get('keys_to_monitor', [])[:5])
            if len(profile.config.get('keys_to_monitor', [])) > 5:
                keys += "..."
            
            # Format modified date
            modified = profile.modified_at.split('T')[0] if 'T' in profile.modified_at else profile.modified_at
            
            self.tree.insert('', tk.END, iid=profile.id, text=is_active,
                           values=(profile.name, keys, modified))
        
        # Clear details
        self._update_details(None)
    
    def _on_profile_selected(self, event):
        """Handle profile selection."""
        selection = self.tree.selection()
        if selection:
            profile_id = selection[0]
            profile = self.profile_manager.get_profile(profile_id)
            self._update_details(profile)
    
    def _on_profile_double_click(self, event):
        """Handle double-click on profile."""
        self._activate_profile()
    
    def _update_details(self, profile):
        """Update the details panel."""
        self.details_text.configure(state=tk.NORMAL)
        self.details_text.delete(1.0, tk.END)
        
        if profile:
            details = f"Profile: {profile.name}\n"
            details += f"ID: {profile.id}\n"
            details += f"Created: {profile.created_at}\n"
            details += f"Modified: {profile.modified_at}\n\n"
            details += "Configuration:\n"
            details += f"  Keys: {', '.join(profile.config.get('keys_to_monitor', []))}\n"
            
            overlay = profile.config.get('overlay', {})
            details += f"  Overlay Size: {overlay.get('width')}x{overlay.get('height')}\n"
            details += f"  Position: ({overlay.get('x')}, {overlay.get('y')})\n"
            
            stats = profile.config.get('statistics', {})
            details += f"  Statistics: {'Enabled' if stats.get('enabled') else 'Disabled'}\n"
            
            animations = profile.config.get('animations', {})
            details += f"  Animations: {animations.get('type', 'none')}\n"
            
            self.details_text.insert(1.0, details)
        else:
            self.details_text.insert(1.0, "No profile selected")
        
        self.details_text.configure(state=tk.DISABLED)
    
    def _create_profile(self):
        """Create a new profile."""
        # Dialog for profile name
        dialog = tk.Toplevel(self.window)
        dialog.title("New Profile")
        dialog.geometry("300x100")
        dialog.transient(self.window)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Profile Name:").pack(pady=(10, 5))
        
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.pack(pady=5)
        name_entry.focus()
        
        def create():
            name = name_entry.get().strip()
            if not name:
                messagebox.showwarning("Invalid Name", 
                                      "Please enter a profile name.")
                return
            
            # Create profile with current config
            current_config = self.config_manager.get_all()
            profile = self.profile_manager.create_profile(name, current_config)
            
            dialog.destroy()
            self._refresh_profile_list()
            
            # Select the new profile
            self.tree.selection_set(profile.id)
            self.tree.see(profile.id)
        
        def cancel():
            dialog.destroy()
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Create", 
                  command=create).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", 
                  command=cancel).pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key
        name_entry.bind('<Return>', lambda e: create())
        dialog.bind('<Escape>', lambda e: cancel())
    
    def _activate_profile(self):
        """Activate the selected profile."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", 
                                  "Please select a profile to activate.")
            return
        
        profile_id = selection[0]
        profile = self.profile_manager.get_profile(profile_id)
        
        if profile:
            # Set as active
            self.profile_manager.set_active_profile(profile_id)
            
            # Update config
            self.config_manager.update(profile.config)
            self.config_manager.save()
            
            # Refresh list
            self._refresh_profile_list()
            
            # Trigger callback
            if self.on_profile_change:
                self.on_profile_change(profile)
            
            messagebox.showinfo("Profile Activated", 
                               f"Profile '{profile.name}' has been activated.")
    
    def _edit_profile(self):
        """Edit the selected profile."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", 
                                  "Please select a profile to edit.")
            return
        
        profile_id = selection[0]
        profile = self.profile_manager.get_profile(profile_id)
        
        if profile:
            # For now, just allow renaming
            # TODO: Add full config editor
            dialog = tk.Toplevel(self.window)
            dialog.title("Edit Profile")
            dialog.geometry("300x100")
            dialog.transient(self.window)
            dialog.grab_set()
            
            ttk.Label(dialog, text="Profile Name:").pack(pady=(10, 5))
            
            name_entry = ttk.Entry(dialog, width=30)
            name_entry.insert(0, profile.name)
            name_entry.pack(pady=5)
            name_entry.focus()
            name_entry.select_range(0, tk.END)
            
            def save():
                new_name = name_entry.get().strip()
                if not new_name:
                    messagebox.showwarning("Invalid Name", 
                                          "Please enter a profile name.")
                    return
                
                profile.name = new_name
                profile.modified_at = profile._generate_id().split('_')[1]
                self.profile_manager.save_profile(profile)
                
                dialog.destroy()
                self._refresh_profile_list()
            
            def cancel():
                dialog.destroy()
            
            button_frame = ttk.Frame(dialog)
            button_frame.pack(pady=10)
            
            ttk.Button(button_frame, text="Save", 
                      command=save).pack(side=tk.LEFT, padx=5)
            ttk.Button(button_frame, text="Cancel", 
                      command=cancel).pack(side=tk.LEFT, padx=5)
            
            name_entry.bind('<Return>', lambda e: save())
            dialog.bind('<Escape>', lambda e: cancel())
    
    def _duplicate_profile(self):
        """Duplicate the selected profile."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", 
                                  "Please select a profile to duplicate.")
            return
        
        profile_id = selection[0]
        profile = self.profile_manager.get_profile(profile_id)
        
        if profile:
            new_name = f"{profile.name} (Copy)"
            new_profile = self.profile_manager.duplicate_profile(profile_id, new_name)
            
            self._refresh_profile_list()
            
            if new_profile:
                self.tree.selection_set(new_profile.id)
                self.tree.see(new_profile.id)
    
    def _delete_profile(self):
        """Delete the selected profile."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", 
                                  "Please select a profile to delete.")
            return
        
        profile_id = selection[0]
        profile = self.profile_manager.get_profile(profile_id)
        
        if profile:
            # Confirm deletion
            if messagebox.askyesno("Confirm Deletion",
                                  f"Are you sure you want to delete profile '{profile.name}'?"):
                self.profile_manager.delete_profile(profile_id)
                self._refresh_profile_list()
    
    def _import_profile(self):
        """Import a profile from file."""
        file_path = filedialog.askopenfilename(
            title="Import Profile",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            profile = self.profile_manager.import_profile(file_path)
            if profile:
                self._refresh_profile_list()
                self.tree.selection_set(profile.id)
                self.tree.see(profile.id)
                messagebox.showinfo("Import Successful",
                                   f"Profile '{profile.name}' has been imported.")
            else:
                messagebox.showerror("Import Failed",
                                    "Failed to import profile.")
    
    def _export_profile(self):
        """Export the selected profile to file."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection",
                                  "Please select a profile to export.")
            return
        
        profile_id = selection[0]
        profile = self.profile_manager.get_profile(profile_id)
        
        if profile:
            file_path = filedialog.asksaveasfilename(
                title="Export Profile",
                defaultextension=".json",
                initialfile=f"{profile.name}.json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if file_path:
                if self.profile_manager.export_profile(profile_id, file_path):
                    messagebox.showinfo("Export Successful",
                                       f"Profile '{profile.name}' has been exported.")
                else:
                    messagebox.showerror("Export Failed",
                                        "Failed to export profile.")
    
    def show(self):
        """Show the window."""
        self.window.deiconify()
    
    def hide(self):
        """Hide the window."""
        self.window.withdraw()
