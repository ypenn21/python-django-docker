from typing import List, Dict, Any

def format_prompt_book_keywords(keywords: List[str]) -> str:
    """
    Formats a prompt to find paragraphs mentioning keywords in a book.

    Args:
        keywords (List[str]): A list of keywords to search for.

    Returns:
        str: The formatted prompt.
    """
    # Filter keywords to remove null or empty strings
    params = [k for k in keywords if k is not None and isinstance(k, str) and k != '']

    if not params:
        return "Find the paragraphs mentioning any topic in the book."  # Or other default message

    # Join the keywords with commas
    joined_keywords = ", ".join(params)

    # Use string formatting to insert the joined keywords into the prompt
    return f"Find the paragraphs mentioning keywords in the following list: {{{joined_keywords}}} in the book."

def format_prompt_book_analysis(book: Dict, book_pages: List[Dict[str, Any]], keywords: List[str]) -> str:
    """
    Formats a prompt for book analysis based on book details, excerpts, and keywords.

    Args:
        book (Dict): A dictionary containing book details (e.g., title, author).
        book_pages (List[Dict[str, Any]]): A list of dictionaries representing book excerpts.
        keywords (List[str]): A list of keywords to analyze.

    Returns:
        str: The formatted prompt for book analysis.
    """
    prompt_book_analysis = """Provide an analysis of the book %s by %s 
        "with the skills of a literary critic.
        "What factor do the following %s
        "play in the narrative of the book.
        "Please use these paragraphs delimited by triple backquotes from the book :\n
        ```%s```
        """

    # Filter keywords to remove null or empty strings
    params = [k for k in keywords if k is not None and isinstance(k, str) and k != '']

    if not params and not book_pages:
        return ""  # Or other default message
    print(params)
    context = " ".join([page.get("page") for page in book_pages])

    return prompt_book_analysis % (
        book.get("book"),
        book.get("author"),
        ", ".join(params),
        context
    )