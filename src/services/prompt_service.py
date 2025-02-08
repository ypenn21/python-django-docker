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

def tf_search_query() -> str:
    return """Find paragraphs mentioning Terraform best practices for general style, structure, and dependency management"""

def format_tf_transform(script: str, context: str) -> str:
    """Formats a prompt for transforming a bash script to Terraform."""

    prompt_tf_transform = """Your task is to translate shell scripts that utilize `gcloud` commands into equivalent, well-structured Terraform code,
        adhering to Terraform best practices for file organization and maintainability.
        Please carefully analyze the provided bash script enclosed within triple back quotes ```{script}```
        
        Your output should include:
        
        1. **Terraform Code in Separate Files:**
           * **main.tf:** A fully functional Terraform configuration file containing the core 
             infrastructure resource definitions that replicate the functionality of the bash script.
           * **variables.tf:** This file should contain all input variable declarations used in 
             the `main.tf` file.
           * **Additional Files (If Applicable):**  Suggest and create additional Terraform files 
             as needed (e.g., `outputs.tf`, `provider.tf`, `data.tf`) based on the complexity and 
             requirements of the converted script.
        
        2. **Explanation:** A clear breakdown of the Terraform resources, variables, and modules 
           used, along with explanations for how they achieve the same results as the original script.
           Indicate which file each element belongs to.
        
        3. **Best Practices:** Where applicable, offer suggestions for adhering to Terraform best 
           practices beyond file organization (e.g., resource naming, input validation, module usage).
        
        4. **Potential Optimizations:** If there are opportunities to make the Terraform code more 
           efficient, concise, or maintainable, please highlight them.
        
        **Important Considerations:**
        
        * **Environment Variables:** If the bash script relies on environment variables, ensure the 
           Terraform code handles them appropriately (e.g., using input variables in `variables.tf`).
        * **Error Handling:** Terraform provides error handling mechanisms that may be missing in the 
           bash script. Incorporate these to improve the robustness of the code.
        * **State Management:** Briefly explain how Terraform state would be managed for this particular 
           configuration.
        * **Example Usage:** Demonstrates how to apply Terraform script.
        * **Reference Documentation:** Output should also consider the following document enclosed within triple back quotes for best practice:
        ```{context}   """
    
    return prompt_tf_transform.format(script=script, context=context)