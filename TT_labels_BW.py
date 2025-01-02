import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib
import textwrap  # For text wrapping
import matplotlib.font_manager as fm

font_path = '/Users/soundtheory/Library/Fonts/Grovana-BoldRough.otf'
custom_font = fm.FontProperties(fname=font_path)

def generate_patch_bay_labels(num_groups, labels_per_group, output_file='test_TT_labels.pdf'):
    """
    Generate a printable patch bay labeling sheet with proper horizontal and vertical spacing, 
    handling overflow, supporting row spanning, and wrapping text.
    
    :param num_groups: Number of 16 TT groupings.
    :param labels_per_group: List of lists, where each sublist contains dictionaries with:
                             'text' (str): The label text,
                             'start' (int): Starting TT position (1-indexed, 1–16 per group),
                             'span' (int): How many TT points the label spans,
                             'row' (str): 'top', 'bottom', or 'both' for spanning rows.
    :param output_file: Output filename for the PDF.
    """
    # Constants for layout
    paper_width, paper_height = 11, 8.5  # Inches
    block_width = 2.75  # Width of each TT block in inches
    block_height = 0.5  # Height of each TT block in inches
    left_margin = 0.625  # Left margin in inches
    block_spacing = 0.375  # Horizontal spacing between blocks in inches
    vertical_spacing = 0.75  # Vertical spacing between rows in inches
    tt_width = block_width / 8  # Width of one TT position
    label_cell_height = block_height / 2  # Height of a single row in the label block
    # wrap_width = 10  # Maximum characters per line for text wrapping. # use for bays 1
    wrap_width = 30  # Maximum characters per line for text wrapping #use for bays 2, 3, 8

    # Font size for labels
    font_size = 8  # Fixed font size to fit within 1 TT span comfortably
    
    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(paper_width, paper_height))
    ax.set_xlim(0, paper_width)
    ax.set_ylim(0, paper_height)
    ax.axis('off')  # Hide axes
    
    # Start drawing at the top-left corner of the page
    start_x, start_y = left_margin, paper_height - 1  # Left margin and top margin
    current_x, current_y = start_x, start_y
    
    for group_index in range(num_groups):
        # Check if the next block fits in the current row
        if current_x + block_width > paper_width:
            # Move to the next row
            current_x = left_margin
            current_y -= (block_height * 2 + vertical_spacing)
        
        # Draw the dummy TT block rectangle
        ax.add_patch(patches.Rectangle((current_x, current_y - block_height), block_width, block_height, fill=False, edgecolor='black'))
        
        # Draw TT positions in the dummy block
        for row in range(2):  # Two rows
            for col in range(8):  # Eight TT points per row
                x = current_x + col * tt_width + tt_width / 2
                y = current_y - row * (block_height / 2) - (block_height / 4)
                ax.add_patch(patches.Circle((x, y), 0.05, color='black'))  # TT point
        
        # Draw the label block rectangle directly below the dummy block
        label_block_y = current_y - block_height * 2
        ax.add_patch(patches.Rectangle((current_x, label_block_y), block_width, block_height, fill=False, edgecolor='black'))
        
        # Add labels and gridlines
        if group_index < len(labels_per_group):
            for label in labels_per_group[group_index]:
                text = label['text']
                start = label['start'] - 1  # Convert to 0-indexed
                span = label['span']
                row = label['row']  # 'top', 'bottom', or 'both'
                
                # Determine label position
                start_x = current_x + (start % 8) * tt_width
                end_x = current_x + ((start + span - 1) % 8) * tt_width + tt_width
                mid_x = (start_x + end_x) / 2
                
                # Wrap the text into multiple lines
                wrapped_text = '\n'.join(textwrap.wrap(text, width=wrap_width))
                
                # Adjust vertical position based on row
                if row == 'top':
                    label_y = label_block_y + (3 / 4) * block_height  # Centered in top row
                elif row == 'bottom':
                    label_y = label_block_y + (1 / 4) * block_height  # Centered in bottom row
                elif row == 'both':
                    label_y = label_block_y + block_height / 2  # Centered across both rows
                else:
                    raise ValueError("Row must be 'top', 'bottom', or 'both'")
                
                # Clip text width to its allocated span
                text_width = end_x - start_x
                text_length = len(text) * 0.07  # Approximate width per character
                if text_length > text_width:  # Scale down font size if text is too wide
                    adjusted_font_size = font_size * (text_width / text_length)
                else:
                    adjusted_font_size = font_size
                
                # Place the label
                ax.text(mid_x, label_y, wrapped_text, ha='center', va='center', fontsize=adjusted_font_size, fontproperties=custom_font, clip_on=True)
                
                # Add solid black gridline (rectangle) around the label's span
                gridline_height = label_cell_height if row in ['top', 'bottom'] else block_height
                ax.add_patch(patches.Rectangle((start_x, label_block_y if row in ['bottom', 'both'] else label_block_y + label_cell_height),
                                               text_width, gridline_height, fill=False, edgecolor='black'))
        
        # Move to the next block position
        current_x += block_width + block_spacing
    
    # Save the output
    plt.savefig(output_file, bbox_inches='tight')
    plt.close()


# Example Dummy Data
labels_per_group = [

# ---------------------------------------------------------------------------------------------
#  PATCHBAY 1
# ---------------------------------------------------------------------------------------------
   
    # # Block 1
    # [
    #     {'text': 'NOHO', 'start': 1, 'span': 2, 'row': 'both'},
    #     {'text': 'LVL', 'start': 3, 'span': 1, 'row': 'both'},
    #     {'text': 'DBX     GML', 'start': 4, 'span': 2, 'row': 'both'},
    #     {'text': '560', 'start': 6, 'span': 1, 'row': 'both'},
    #     {'text': 'DS', 'start': 7, 'span': 1, 'row': 'both'},
    #     {'text': '-', 'start': 8, 'span': 1, 'row': 'both'},
    
    # ],
    # # Block 2
    # [
    #     {'text': 'ADR', 'start': 1, 'span': 2, 'row': 'both'},
    #     {'text': '162', 'start': 3, 'span': 2, 'row': 'both'},
    #     {'text': 'PIE', 'start': 5, 'span': 2, 'row': 'both'},
    #     {'text': 'LA4', 'start': 7, 'span': 2, 'row': 'both'},

    #     # {'text': 'IJ', 'start': 1, 'span': 2, 'row': 'bottom'},
     
    #     # {'text': 'MN', 'start': 5, 'span': 2, 'row': 'bottom'},
    

    # ],
    # # Block 3
    # [
    #     {'text': 'DYNA', 'start': 1, 'span': 2, 'row': 'both'},
    #     {'text': 'GBUS', 'start': 3, 'span': 2, 'row': 'both'},
    #     {'text': 'CLARI', 'start': 5, 'span': 2, 'row': 'both'},
    #     {'text': 'TUN  ', 'start': 7, 'span': 1, 'row': 'both'},
    #     {'text': 'SAN  ', 'start': 8, 'span': 1, 'row': 'both'},

    # ],
    # # Block 4
    # [
    #     {'text': 'GMAJ', 'start': 1, 'span': 2, 'row': 'both'},
    #     {'text': 'SPX90', 'start': 3, 'span': 2, 'row': 'both'},
    #     {'text': 'SPX90II', 'start': 5, 'span': 2, 'row': 'both'},
    #     {'text': 'DAK  ', 'start': 7, 'span': 1, 'row': 'both'},
    #     {'text': 'BL40  ', 'start': 8, 'span': 1, 'row': 'both'},

    # ],

    #     # Block 5
    # [
    #     {'text': 'IBP 2-3', 'start': 1, 'span': 2, 'row': 'both'},
    #     {'text': 'DIS', 'start': 3, 'span': 1, 'row': 'both'},
    #     {'text': '1176 ', 'start': 4, 'span': 1, 'row': 'both'},
    #     {'text': '-', 'start': 5, 'span': 4, 'row': 'top'},
    #     {'text': 'BRULE 1-4', 'start': 5, 'span': 4, 'row': 'bottom'},

    # ],

    #     # Block 6
    # [
    #     {'text': 'TEAC 1-4', 'start': 1, 'span': 4, 'row': 'both'},
    #     {'text': 'AMS     REV', 'start': 5, 'span': 2, 'row': 'both'},
    #     {'text': 'AMS   DELAY', 'start': 7, 'span': 2, 'row': 'both'},

    # ],

    #     # Block 7
    # [
    #     {'text': 'DEP', 'start': 1, 'span': 1, 'row': 'both'},
    #     {'text': 'WOW', 'start': 2, 'span': 2, 'row': 'both'},
    #     {'text': 'LIGHT', 'start': 4, 'span': 2, 'row': 'both'},
    #     {'text': 'TAPE   DECK', 'start': 6, 'span': 2, 'row': 'both'},
    #     {'text': '-', 'start': 8, 'span': 1, 'row': 'both'},
    # ],


# ---------------------------------------------------------------------------------------------
#  PATCHBAY 2
# ---------------------------------------------------------------------------------------------
        # Block 1
    # [
    #     {'text': 'MCI OUT 1-8', 'start': 1, 'span': 8, 'row': 'top'},
    #     {'text': 'TASCAM IN 1-8', 'start': 1, 'span': 8, 'row': 'bottom'},

    # ],

    #     # Block 2
    # [
    #     {'text': 'MCI OUT 9-16', 'start': 1, 'span': 8, 'row': 'top'},
    #     {'text': 'TASCAM IN 9-16', 'start': 1, 'span': 8, 'row': 'bottom'},
    # ],

    #     # Block 3
    # [
    #     {'text': 'MCI OUT 17-24', 'start': 1, 'span': 8, 'row': 'top'},
    #     {'text': 'TASCAM IN 17-24', 'start': 1, 'span': 8, 'row': 'bottom'},
    # ],

    #     # Block 4
    # [
    #     {'text': 'PUMPKIN TRACK OUT 25-32', 'start': 1, 'span': 8, 'row': 'top'},
    #     {'text': 'TASCAM IN 25-32', 'start': 1, 'span': 8, 'row': 'bottom'},
    # ],

    #      # Block 5
    # [
    #     {'text': 'PUMPKIN TRACK OUT 1-8', 'start': 1, 'span': 8, 'row': 'top'},
    #     {'text': 'MCI IN 1- 8', 'start': 1, 'span': 8, 'row': 'bottom'},
    # ],

    #      # Block 6
    # [
    #     {'text': 'PUMPKIN TRACK OUT 9-16', 'start': 1, 'span': 8, 'row': 'top'},
    #     {'text': 'MCI IN 9- 16', 'start': 1, 'span': 8, 'row': 'bottom'},
    # ],

    #      # Block 7
    # [
    #     {'text': 'PUMPKIN TRACK OUT 17-24', 'start': 1, 'span': 8, 'row': 'top'},
    #     {'text': 'MCI IN 17-24', 'start': 1, 'span': 8, 'row': 'bottom'},
    # ],

# ---------------------------------------------------------------------------------------------
#  PATCHBAY 3
# ---------------------------------------------------------------------------------------------

#         # Block 1
#     [
#         {'text': 'CHANNEL DIRECT OUT 1-8', 'start': 1, 'span': 8, 'row': 'top'},
#         {'text': 'CHANNEL DIRECT OUT 25-32', 'start': 1, 'span': 8, 'row': 'bottom'},

#     ],

#         # Block 2
#     [
#         {'text': 'CHANNEL DIRECT OUT 9-16', 'start': 1, 'span': 8, 'row': 'top'},
#         {'text': 'CHANNEL DIRECT OUT 33-40', 'start': 1, 'span': 8, 'row': 'bottom'},
#     ],

#         # Block 3
#     [
#         {'text': 'CHANNEL DIRECT OUT 17-24', 'start': 1, 'span': 8, 'row': 'top'},
#         {'text': 'CHANNEL DIRECT OUT 41-48', 'start': 1, 'span': 8, 'row': 'bottom'},
#     ],

#         # Block 4
#     [
#         {'text': 'PUMPKIN 4T 1-4', 'start': 1, 'span': 4, 'row': 'top'},
#         {'text': 'SPEAKERS    ', 'start': 5, 'span': 2, 'row': 'top'},
#         {'text': '-', 'start': 1, 'span': 8, 'row': 'bottom'},
#     ],
# ]

# ---------------------------------------------------------------------------------------------
#  PATCHBAY 8
# ---------------------------------------------------------------------------------------------

        # Block 1
    [
        {'text': 'REV RETURN IN', 'start': 1, 'span': 4, 'row': 'both'},
        {'text': '-', 'start': 5, 'span': 4, 'row': 'both'},


    ],

        # Block 2
    [
        {'text': 'TASCAM OUT 1-8', 'start': 1, 'span': 8, 'row': 'top'},
        {'text': 'LINE IN 1-8', 'start': 1, 'span': 8, 'row': 'bottom'},
    ],

        # Block 3
    [
        {'text': 'TASCAM OUT 9-16', 'start': 1, 'span': 8, 'row': 'top'},
        {'text': 'LINE IN 9-16', 'start': 1, 'span': 8, 'row': 'bottom'},
    ],

        # Block 4
    [
        {'text': 'TASCAM OUT 17-24', 'start': 1, 'span': 8, 'row': 'top'},
        {'text': 'LINE IN 17-24', 'start': 1, 'span': 8, 'row': 'bottom'},
    ],
        # Block 5
    [
        {'text': 'TASCAM OUT 25-32', 'start': 1, 'span': 8, 'row': 'top'},
        {'text': 'LINE IN 25-32', 'start': 1, 'span': 8, 'row': 'bottom'},
    ],

        # Block 6
    [
        {'text': '-', 'start': 1, 'span': 8, 'row': 'top'},
        {'text': 'LINE IN 33-40', 'start': 1, 'span': 8, 'row': 'bottom'},

    ],

        # Block 7
    [
        {'text': '-', 'start': 1, 'span': 8, 'row': 'top'},
        {'text': 'LINE IN 41-48', 'start': 1, 'span': 8, 'row': 'bottom'},
    ],
]


# Generate the labels with blocks
generate_patch_bay_labels(12, labels_per_group)
