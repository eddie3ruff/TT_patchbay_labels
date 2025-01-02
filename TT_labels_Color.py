
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import textwrap
import matplotlib.font_manager as fm

class PatchBayLabelGenerator:
    def __init__(self, font_path, paper_width=11, paper_height=8.5):
        """
        Initialize the PatchBayLabelGenerator.

        :param font_path: Path to the custom font file.
        :param paper_width: Width of the paper in inches.
        :param paper_height: Height of the paper in inches.
        """
        self.font_path = font_path
        self.custom_font = fm.FontProperties(fname=font_path)
        self.paper_width = paper_width
        self.paper_height = paper_height
        self.block_width = 2.85 #2.75
        self.block_height = 0.5
        self.left_margin = 0.625
        self.block_spacing = 0.55 #0.375
        self.vertical_spacing = 0.75
        self.tt_width = self.block_width / 8
        self.label_cell_height = self.block_height / 2
        self.wrap_width = 10
        # self.wrap_width = 30
        self.font_size = 8

    def generate_labels(self, num_groups, labels_per_group, output_file='output_labels.pdf'):
        """
        Generate a printable patch bay labeling sheet.

        :param num_groups: Number of TT groupings.
        :param labels_per_group: List of label data for each group.
        :param output_file: Path to save the generated PDF.
        """
        fig, ax = plt.subplots(figsize=(self.paper_width, self.paper_height))
        ax.set_xlim(0, self.paper_width)
        ax.set_ylim(0, self.paper_height)
        ax.axis('off')

        start_x, start_y = self.left_margin, self.paper_height - 1
        current_x, current_y = start_x, start_y

        for group_index in range(num_groups):
            if current_x + self.block_width > self.paper_width:
                current_x = self.left_margin
                current_y -= (self.block_height * 2 + self.vertical_spacing)

            ax.add_patch(patches.Rectangle(
                (current_x, current_y - self.block_height),
                self.block_width,
                self.block_height,
                fill=False,
                edgecolor='black'
            ))

            for row in range(2):
                for col in range(8):
                    x = current_x + col * self.tt_width + self.tt_width / 2
                    y = current_y - row * (self.block_height / 2) - (self.block_height / 4)
                    ax.add_patch(patches.Circle((x, y), 0.05, color='black'))

            label_block_y = current_y - self.block_height * 2
            ax.add_patch(patches.Rectangle(
                (current_x, label_block_y),
                self.block_width,
                self.block_height,
                fill=False,
                edgecolor='black'
            ))

            if group_index < len(labels_per_group):
                for label in labels_per_group[group_index]:
                    text = label['text']
                    start = label['start'] - 1
                    span = label['span']
                    row = label['row']
                    label_color = label.get('color', None)

                    start_x_label = current_x + (start % 8) * self.tt_width
                    end_x_label = current_x + ((start + span - 1) % 8) * self.tt_width + self.tt_width
                    text_width = end_x_label - start_x_label
                    mid_x = (start_x_label + end_x_label) / 2

                    wrapped_text = '\n'.join(textwrap.wrap(text, width=self.wrap_width))

                    if row == 'top':
                        label_y = label_block_y + (3 / 4) * self.block_height
                        rect_y = label_block_y + self.label_cell_height
                        rect_height = self.label_cell_height
                    elif row == 'bottom':
                        label_y = label_block_y + (1 / 4) * self.block_height
                        rect_y = label_block_y
                        rect_height = self.label_cell_height
                    elif row == 'both':
                        label_y = label_block_y + (self.block_height / 2)
                        rect_y = label_block_y
                        rect_height = self.block_height
                    else:
                        raise ValueError("Row must be 'top', 'bottom', or 'both'.")

                    text_length_approx = len(text) * 0.07
                    if text_length_approx > text_width:
                        adjusted_font_size = self.font_size * (text_width / text_length_approx)
                    else:
                        adjusted_font_size = self.font_size

                    if label_color is not None:
                        ax.add_patch(patches.Rectangle(
                            (start_x_label, rect_y),
                            text_width,
                            rect_height,
                            fill=True,
                            facecolor=label_color,
                            # alpha=0.5,
                            alpha=1.0,
                            edgecolor=None,
                            zorder=1
                        ))

                    ax.add_patch(patches.Rectangle(
                        (start_x_label, rect_y),
                        text_width,
                        rect_height,
                        fill=False,
                        edgecolor='black',
                        zorder=2
                    ))

                    ax.text(
                        mid_x, label_y,
                        wrapped_text,
                        ha='center',
                        va='center',
                        fontsize=adjusted_font_size,
                        fontproperties=self.custom_font,
                        clip_on=True,
                        zorder=3
                    )

            current_x += self.block_width + self.block_spacing

        plt.savefig(output_file, bbox_inches='tight')
        plt.close()

# Example Usage
font_path = '/Users/soundtheory/Library/Fonts/Grovana-BoldRough.otf'
generator = PatchBayLabelGenerator(font_path)

labels_per_group = [

# ---------------------------------------------------------------------------------------------
#  PATCHBAY 1
# ---------------------------------------------------------------------------------------------
   
    # Block 1
    [
        {'text': 'NOHO', 'start': 1, 'span': 2, 'row': 'both', 'color': '#ED663D'},
        {'text': 'LVL', 'start': 3, 'span': 1, 'row': 'both', 'color': '#ED663D'},
        {'text': 'DBX     GML', 'start': 4, 'span': 2, 'row': 'both', 'color': '#33787E'},
        {'text': '560', 'start': 6, 'span': 1, 'row': 'both', 'color': '#33787E'},
        {'text': 'DS', 'start': 7, 'span': 1, 'row': 'both', 'color': '#33787E'},
        {'text': '-', 'start': 8, 'span': 1, 'row': 'both', 'color': '#F7C561'},
    
    ],
    # Block 2
    [
        {'text': 'ADR', 'start': 1, 'span': 2, 'row': 'both', 'color': '#33787E'},
        {'text': '162', 'start': 3, 'span': 2, 'row': 'both', 'color': '#33787E'},
        {'text': 'PIE', 'start': 5, 'span': 2, 'row': 'both', 'color': '#33787E'},
        {'text': 'LA4', 'start': 7, 'span': 2, 'row': 'both', 'color': '#33787E'},

        # {'text': 'IJ', 'start': 1, 'span': 2, 'row': 'bottom'},
     
        # {'text': 'MN', 'start': 5, 'span': 2, 'row': 'bottom'},
    

    ],
    # Block 3
    [
        {'text': 'DYNA', 'start': 1, 'span': 2, 'row': 'both', 'color': '#33787E'},
        {'text': 'GBUS', 'start': 3, 'span': 2, 'row': 'both', 'color': '#33787E'},
        {'text': 'CLARI', 'start': 5, 'span': 2, 'row': 'both', 'color': '#ED663D'},
        {'text': 'TUN  ', 'start': 7, 'span': 1, 'row': 'both', 'color': '#F7C561'},
        {'text': 'SAN  ', 'start': 8, 'span': 1, 'row': 'both', 'color': '#ED663D'},

    ],
    # Block 4
    [
        {'text': 'GMAJ', 'start': 1, 'span': 2, 'row': 'both', 'color': '#387EC9'},
        {'text': 'SPX90', 'start': 3, 'span': 2, 'row': 'both', 'color': '#387EC9'},
        {'text': 'SPX90II', 'start': 5, 'span': 2, 'row': 'both', 'color': '#387EC9'},
        {'text': 'DAK  ', 'start': 7, 'span': 1, 'row': 'both', 'color': '#ED663D'},
        {'text': 'BL40  ', 'start': 8, 'span': 1, 'row': 'both', 'color': '#33787E'},

    ],

        # Block 5
    [
        {'text': 'IBP 2-3', 'start': 1, 'span': 2, 'row': 'both', 'color': '#387EC9'},
        {'text': 'DIS', 'start': 3, 'span': 1, 'row': 'both', 'color': '#33787E'},
        {'text': '1176 ', 'start': 4, 'span': 1, 'row': 'both', 'color': '#33787E'},
        {'text': '-', 'start': 5, 'span': 4, 'row': 'top', 'color': '#F7C561'},
        {'text': 'BRULE 1-4', 'start': 5, 'span': 4, 'row': 'bottom', 'color': '#ED663D'},

    ],

        # Block 6
    [
        {'text': 'TEAC 1-4', 'start': 1, 'span': 4, 'row': 'both', 'color': '#7E4C8D'},
        {'text': 'AMS     REV', 'start': 5, 'span': 2, 'row': 'both', 'color': '#387EC9'},
        {'text': 'AMS   DELAY', 'start': 7, 'span': 2, 'row': 'both', 'color': '#387EC9'},

    ],

        # Block 7
    [
        {'text': 'DEP', 'start': 1, 'span': 1, 'row': 'both', 'color': '#33787E'},
        {'text': 'WOW', 'start': 2, 'span': 2, 'row': 'both', 'color': '#387EC9'},
        {'text': 'BULB  ', 'start': 4, 'span': 1, 'row': 'both', 'color': '#ED663D'},
        {'text': 'SPRING', 'start': 5, 'span': 2, 'row': 'both', 'color': '#387EC9'},
        {'text': 'TAPE   DECK', 'start': 7, 'span': 2, 'row': 'both', 'color': '#7E4C8D'},
    
    ],

# # ---------------------------------------------------------------------------------------------
# #  PATCHBAY 2
# # ---------------------------------------------------------------------------------------------
        
    #     # Block 1
    # [
    #     {'text': 'MCI OUT 1-8', 'start': 1, 'span': 8, 'row': 'top', 'color': '#7E4C8D'},
    #     {'text': 'TASCAM IN 1-8', 'start': 1, 'span': 8, 'row': 'bottom', 'color': '#33787E'},

    # ],

    #     # Block 2
    # [
    #     {'text': 'MCI OUT 9-16', 'start': 1, 'span': 8, 'row': 'top', 'color': '#7E4C8D'},
    #     {'text': 'TASCAM IN 9-16', 'start': 1, 'span': 8, 'row': 'bottom', 'color': '#33787E'},
    # ],

    #     # Block 3
    # [
    #     {'text': 'MCI OUT 17-24', 'start': 1, 'span': 8, 'row': 'top', 'color': '#7E4C8D'},
    #     {'text': 'TASCAM IN 17-24', 'start': 1, 'span': 8, 'row': 'bottom', 'color': '#33787E'},
    # ],

    #     # Block 4
    # [
    #     {'text': 'PUMPKIN TRACK OUT 25-32', 'start': 1, 'span': 8, 'row': 'top', 'color': '#ED663D'},
    #     {'text': 'TASCAM IN 25-32', 'start': 1, 'span': 8, 'row': 'bottom', 'color': '#33787E'},
    # ],

    #      # Block 5
    # [
    #     {'text': 'PUMPKIN TRACK OUT 1-8', 'start': 1, 'span': 8, 'row': 'top', 'color': '#ED663D'},
    #     {'text': 'MCI IN 1- 8', 'start': 1, 'span': 8, 'row': 'bottom', 'color': '#7E4C8D'},
    # ],

    #      # Block 6
    # [
    #     {'text': 'PUMPKIN TRACK OUT 9-16', 'start': 1, 'span': 8, 'row': 'top', 'color': '#ED663D'},
    #     {'text': 'MCI IN 9- 16', 'start': 1, 'span': 8, 'row': 'bottom', 'color': '#7E4C8D'},
    # ],

    #      # Block 7
    # [
    #     {'text': 'PUMPKIN TRACK OUT 17-24', 'start': 1, 'span': 8, 'row': 'top', 'color': '#ED663D'},
    #     {'text': 'MCI IN 17-24', 'start': 1, 'span': 8, 'row': 'bottom', 'color': '#7E4C8D'},
    # ],


    # [
    #     {'text': 'REV RETURN IN', 'start': 1, 'span': 4, 'row': 'both', 'color': '#F35A1B'},
    #     {'text': '-', 'start': 5, 'span': 4, 'row': 'both', 'color': '#CCFFCC'}
    # ],
    # [
    #     {'text': 'TASCAM OUT 1-8', 'start': 1, 'span': 8, 'row': 'top', 'color': '#CCCCFF'},
    #     {'text': 'LINE IN 1-8', 'start': 1, 'span': 8, 'row': 'bottom', 'color': '#FFFFCC'}
    # ]

# # ---------------------------------------------------------------------------------------------
# #  PATCHBAY 3
# # ---------------------------------------------------------------------------------------------

        # Block 1
    # [
    #     {'text': 'CHANNEL DIRECT OUT 1-8', 'start': 1, 'span': 8, 'row': 'top'},
    #     {'text': 'CHANNEL DIRECT OUT 25-32', 'start': 1, 'span': 8, 'row': 'bottom'},

    # ],

    #     # Block 2
    # [
    #     {'text': 'CHANNEL DIRECT OUT 9-16', 'start': 1, 'span': 8, 'row': 'top'},
    #     {'text': 'CHANNEL DIRECT OUT 33-40', 'start': 1, 'span': 8, 'row': 'bottom'},
    # ],

    #     # Block 3
    # [
    #     {'text': 'CHANNEL DIRECT OUT 17-24', 'start': 1, 'span': 8, 'row': 'top'},
    #     {'text': 'CHANNEL DIRECT OUT 41-48', 'start': 1, 'span': 8, 'row': 'bottom'},
    # ],

    #     # Block 4
    # [
    #     {'text': 'PUMPKIN 4T 1-4', 'start': 1, 'span': 4, 'row': 'top', 'color': '#ED663D'},
    #     {'text': 'SPEAKERS    ', 'start': 5, 'span': 2, 'row': 'top', 'color': '#387EC9'},
    #     {'text': '-', 'start': 7, 'span': 2, 'row': 'top', 'color': '#F7C561'},
    #     {'text': '-', 'start': 1, 'span': 8, 'row': 'bottom', 'color': '#F7C561'},
    # ],
       
    #     # Block 5
    # [
    #     {'text': '-', 'start': 1, 'span': 8, 'row': 'both', 'color': '#F7C561'},
    # ],

    #         # Block 6
    # [
    #     {'text': '-', 'start': 1, 'span': 8, 'row': 'both', 'color': '#F7C561'},
    # ],

    #         # Block 7
    # [
    #     {'text': '-', 'start': 1, 'span': 8, 'row': 'both', 'color': '#F7C561'},
    # ],


# ---------------------------------------------------------------------------------------------
#  PATCHBAY 8
# ---------------------------------------------------------------------------------------------

    #     # Block 1
    # [
    #     {'text': 'REV RETURN IN', 'start': 1, 'span': 4, 'row': 'both'},
    #     {'text': '-', 'start': 5, 'span': 4, 'row': 'both'},


    # ],

    #     # Block 2
    # [
    #     {'text': 'TASCAM OUT 1-8', 'start': 1, 'span': 8, 'row': 'top'},
    #     {'text': 'LINE IN 1-8', 'start': 1, 'span': 8, 'row': 'bottom'},
    # ],

    #     # Block 3
    # [
    #     {'text': 'TASCAM OUT 9-16', 'start': 1, 'span': 8, 'row': 'top'},
    #     {'text': 'LINE IN 9-16', 'start': 1, 'span': 8, 'row': 'bottom'},
    # ],

    #     # Block 4
    # [
    #     {'text': 'TASCAM OUT 17-24', 'start': 1, 'span': 8, 'row': 'top'},
    #     {'text': 'LINE IN 17-24', 'start': 1, 'span': 8, 'row': 'bottom'},
    # ],
    #     # Block 5
    # [
    #     {'text': 'TASCAM OUT 25-32', 'start': 1, 'span': 8, 'row': 'top'},
    #     {'text': 'LINE IN 25-32', 'start': 1, 'span': 8, 'row': 'bottom'},
    # ],

    #     # Block 6
    # [
    #     {'text': '-', 'start': 1, 'span': 8, 'row': 'top'},
    #     {'text': 'LINE IN 33-40', 'start': 1, 'span': 8, 'row': 'bottom'},

    # ],

    #     # Block 7
    # [
    #     {'text': '-', 'start': 1, 'span': 8, 'row': 'top'},
    #     {'text': 'LINE IN 41-48', 'start': 1, 'span': 8, 'row': 'bottom'},
    # ],
    ]

generator.generate_labels(7, labels_per_group, output_file='example_labels.pdf')



# GREEN #33787E
# ORANGE #ED663D
# BLUE #387EC9
# YELLOW #FBCE32
# BLANK/FILLER #F7C561
# RED #E82D2E
# PURPLE #7E4C8D

#print landscape at 123% scale