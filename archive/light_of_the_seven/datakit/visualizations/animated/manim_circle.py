"""
Animated visualization of the Circle of Fifths using Manim.

This script generates a step-by-step animation of the Circle of Fifths as:
- A finite state machine (FSM).
- A graph traversal algorithm.
- A logic-based system (Boolean algebra, qubits).
"""

from manim import *


class CircleOfFifths(Scene):
    def construct(self):
        # Define the Circle of Fifths keys
        keys = ["C", "G", "D", "A", "E", "B", "F#", "C#", "G#", "D#", "A#", "F"]
        num_keys = len(keys)

        # Create the circle
        circle = Circle(radius=3, color=BLUE)
        self.play(Create(circle))
        self.wait(1)

        # Add keys as labels
        key_labels = VGroup()
        for i, key in enumerate(keys):
            angle = i * (2 * PI / num_keys) - PI / 2
            label = Text(key, font_size=24).move_to(circle.point_at_angle(angle) * 1.1)
            key_labels.add(label)

        self.play(Write(key_labels))
        self.wait(1)

        # Highlight transitions (perfect fifths)
        for i in range(num_keys):
            start_angle = i * (2 * PI / num_keys) - PI / 2
            end_angle = ((i + 1) % num_keys) * (2 * PI / num_keys) - PI / 2

            # Draw the transition arrow
            arrow = Arrow(
                circle.point_at_angle(start_angle),
                circle.point_at_angle(end_angle),
                color=YELLOW,
                buff=0.2,
                stroke_width=3,
            )

            # Add transition label (e.g., "Perfect Fifth")
            transition_label = Text("Perfect Fifth", font_size=18).next_to(
                arrow, UP, buff=0.1
            )

            self.play(
                GrowArrow(arrow),
                Write(transition_label),
            )
            self.wait(0.5)
            self.play(
                FadeOut(arrow),
                FadeOut(transition_label),
            )

        # Explain the Circle as an FSM
        fsm_title = Text("Circle of Fifths as a Finite State Machine", font_size=28)
        fsm_title.to_edge(UP)
        self.play(Write(fsm_title))
        self.wait(1)

        fsm_explanation = BulletedList(
            "Each key is a state.",
            "Transitions are perfect fifths.",
            "Moving clockwise adds sharps.",
            "Moving counterclockwise adds flats.",
            font_size=20,
        )
        fsm_explanation.next_to(fsm_title, DOWN, buff=0.5)
        self.play(Write(fsm_explanation))
        self.wait(3)

        # Clear the scene
        self.play(
            FadeOut(fsm_title),
            FadeOut(fsm_explanation),
            FadeOut(key_labels),
            FadeOut(circle),
        )
        self.wait(1)

        # Explain the Circle as a logic system
        logic_title = Text("Circle of Fifths as a Logic System", font_size=28)
        logic_title.to_edge(UP)
        self.play(Write(logic_title))
        self.wait(1)

        logic_explanation = BulletedList(
            "Keys = States (e.g., qubits).",
            "Intervals = Logic gates (e.g., AND, OR).",
            "Chord progressions = Boolean algebra.",
            "Modulation = State transitions.",
            font_size=20,
        )
        logic_explanation.next_to(logic_title, DOWN, buff=0.5)
        self.play(Write(logic_explanation))
        self.wait(3)

        # Clear the scene
        self.play(
            FadeOut(logic_title),
            FadeOut(logic_explanation),
        )
        self.wait(1)

        # Recreate the Circle of Fifths for the final animation
        circle = Circle(radius=3, color=BLUE)
        self.play(Create(circle))

        key_labels = VGroup()
        for i, key in enumerate(keys):
            angle = i * (2 * PI / num_keys) - PI / 2
            label = Text(key, font_size=24).move_to(circle.point_at_angle(angle) * 1.1)
            key_labels.add(label)

        self.play(Write(key_labels))
        self.wait(1)

        # Animate a chord progression (e.g., I-IV-V-I in C)
        progression = ["C", "F", "G", "C"]
        progression_labels = VGroup()

        for key in progression:
            index = keys.index(key)
            angle = index * (2 * PI / num_keys) - PI / 2
            dot = Dot(circle.point_at_angle(angle), color=RED, radius=0.15)
            label = Text(key, font_size=24, color=RED).next_to(dot, UP, buff=0.2)
            progression_labels.add(VGroup(dot, label))

        for i, label_group in enumerate(progression_labels):
            self.play(
                FadeIn(label_group[0]),  # Dot
                Write(label_group[1]),  # Label
            )
            self.wait(1)

            if i < len(progression) - 1:
                # Highlight the transition
                start_key = progression[i]
                end_key = progression[i + 1]
                start_index = keys.index(start_key)
                end_index = keys.index(end_key)

                start_angle = start_index * (2 * PI / num_keys) - PI / 2
                end_angle = end_index * (2 * PI / num_keys) - PI / 2

                arrow = Arrow(
                    circle.point_at_angle(start_angle),
                    circle.point_at_angle(end_angle),
                    color=GREEN,
                    buff=0.2,
                    stroke_width=3,
                )
                self.play(GrowArrow(arrow))
                self.wait(1)
                self.play(FadeOut(arrow))

        # Final message
        final_message = Text("The Circle of Fifths as an Algorithm", font_size=32)
        final_message.to_edge(DOWN)
        self.play(Write(final_message))
        self.wait(3)
