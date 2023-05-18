from pptx import Presentation


def parse_pptx_content_to_string_dict(pptx_path):
    """
    Parses the content of a PowerPoint file and returns a dictionary with slide numbers as keys and
    slide content as string values.

    :param pptx_path: The path to the PowerPoint file.
    :return: A dictionary with slide numbers as keys and slide content as string values.
    """
    presentation = Presentation(pptx_path)
    parsed_content = {}

    for i, slide in enumerate(presentation.slides, start=1):
        slide_content = ""

        for shape in slide.shapes:
            if shape.has_text_frame:
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        slide_content += run.text
        # Only slides with non-empty content will be included
        if slide_content:
            parsed_content[i] = slide_content

    return parsed_content
