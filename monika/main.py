from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
from datetime import datetime
from kivy.core.window import Window

class MentalApp(MDApp):

    def build(self):
        # # Create a root layout (Box Layout) for the entire screen
        # root_layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        # Create a root layout (Box Layout) for the entire screen
        root_layout = BoxLayout(orientation='vertical', spacing=10, padding=20, size_hint_y=None)

        # Set the minimum height of the layout
        root_layout.bind(minimum_height=root_layout.setter('height'))

        # Title
        title_label = MDLabel(text="Weekly Wellness Check-in", font_style='H4')
        root_layout.add_widget(title_label)

        # Name input in a container
        name_container = BoxLayout(orientation='horizontal')
        name_label = MDLabel(text="Enter your name:")
        self.name_input = MDTextField(hint_text="Your Name")
        name_container.add_widget(name_label)
        name_container.add_widget(self.name_input)
        root_layout.add_widget(name_container)

        # Days of the week
        self.day_inputs = {}

        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        # Create UI components for each day
        for day in days:
            label = MDLabel(text=day, size_hint_y=None, height=30)
            text_input = MDTextField(hint_text=f"How is your mood on {day}? (1 to 5)", size_hint_y=None, height=30)
            root_layout.add_widget(label)
            root_layout.add_widget(text_input)

            # Save the number input from the user to the array
            self.day_inputs[day] = text_input

        # Create a button to trigger the check-in
        check_in_button = MDRaisedButton(text="Check-in", on_release=self.show_summary)
        root_layout.add_widget(check_in_button)

        # # Create a ScrollView and add the entire UI layout to it
        # scroll_view = ScrollView()
        # scroll_view.add_widget(root_layout)

        # Create a ScrollView and add the entire UI layout to it
        scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        scroll_view.add_widget(root_layout)

        return scroll_view

    def show_summary(self, instance):
        name = self.name_input.text

        # Collect mood ratings for each day
        mood_ratings = {}

        # Iterate over the items in self.day_inputs
        for day, text_input in self.day_inputs.items():

            # Get the mood rating from the text input
            mood_rating = text_input.text

            # Check if mood_rating is a digit before attempting to convert to int
            if mood_rating.isdigit():
                mood_ratings[day] = int(mood_rating)
            else:
                self.show_error_dialog(f"Please enter a valid integer mood rating for {day}")

        # Perform any necessary validation or further processing
        if all(1 <= rating <= 5 for rating in mood_ratings.values()):
            self.save_check_in(name, mood_ratings)

            # Calculate the average mood rating
            average_rating = sum(mood_ratings.values()) / len(mood_ratings)

            # Get additional information based on the average rating
            additional_info = self.get_additional_info(average_rating)

            # Display the summary pop-up with average rating and additional information
            self.show_summary_popup(name, mood_ratings, average_rating, additional_info)
        else:
            self.show_error_dialog("Please enter valid mood ratings between 1 and 5 for each day.")

    def show_error_dialog(self, message):
        dialog = MDDialog(title="Error", text=message, size_hint=(0.8, 0.4))
        dialog.open()

    def save_check_in(self, name, mood_ratings):
        today = datetime.now().date()
        with open(f"check_ins_{today}.txt", "a") as file:
            file.write(f"{name}: Mood ratings - {mood_ratings}\n")

    def get_additional_info(self, average_rating):
        if 1 <= average_rating < 3:
            return "Your mood indicates it's a challenging time for you. Reach out for support if needed."
        elif 3 <= average_rating < 5:
            return "You're doing okay. Keep up the good work!"
        elif average_rating == 5:
            return "Fantastic! Your mood suggests you're having a great week!"
        else:
            return ""

    def show_summary_popup(self, name, mood_ratings, average_rating, additional_info):
        summary_text = f"Check-in summary for {name}:\n {mood_ratings}\n\n" \
                       f"Average Mood Rating: {average_rating:.2f}\n" \
                       f"{additional_info}"

        dialog = MDDialog(
            title="Check-in Summary",
            text=summary_text,
            buttons=[
                MDRaisedButton(text="OK", on_release=lambda *args: self.dialog_dismiss(dialog))
            ],
        )

        dialog.open()

    def dialog_dismiss(self, dialog):
        dialog.dismiss()

if __name__ == "__main__":
    MentalApp().run()
