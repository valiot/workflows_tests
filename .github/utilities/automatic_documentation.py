"""
Script to automate the creation of
automatic documentation with MkDocs
"""
import os
import shutil
import re
from typing import List, Union, Dict
from datetime import datetime as date
from pathlib import Path
from copy import deepcopy


def prettify_text(text: str) -> str:
    """Parse a string into understandable  and pretty text
    Args:
    --------
        - text (str): Text to parse into readable and pretty text.
    Returns:
    ---------
        - Return the same initial text but prettify
    """
    # First, if you find any "-" or "_", change it for " "
    text = text.replace("-", " ").replace("_", " ")
    # If for some reason, we have an .py in the title, we'd erase it as well.
    text = text.replace(".py", "")
    # Now, ensure that each word it's capitalized in the word (only if the word it's
    # separated by an spate or underscore. Otherwise, only capitalize the first letter).
    text = " ".join(word[0].upper()+word[1:-1]+word[-1]
                    for word in text.split(" ") if word)
    return text


def remove_docs_before_create(folder: str) -> None:
    """Remove the documentation before creating new one.
    Args:
    ------
        - folder (str): Folder that contains the documentation
    """
    path = Path(f"docs/{folder}")
    # If this path exists and is a directory, remove it
    if path.is_dir():
        shutil.rmtree(path)
    # Now, if it was remove it, create it again with a .gitignore
    docs = Path("docs/"+folder+"/.gitignore")
    docs.parent.mkdir(parents=True, exist_ok=True)
    with docs.open("w", encoding="utf-8") as gitignore:
        gitignore.write(
            "# Don't count any created file to upload from this folder\n*")
    gitignore.close()


def obtain_paths(folder: str) -> Dict[str, Union[list, dict, str]]:
    """From the main repo folder, obtain not only the modules names
    also obtain the sub-module names (in case that there exist) and the
    files names.
    """
    intern_paths = {
        "Documentation": "",  # Here, would go the __init__.py
        "Main files": {},  # Here, would go any main file,
    }
    # Initialize the folder as path
    for item in Path(folder).iterdir():
        if item.is_dir() and not str(item).startswith("."):
            # Grab only the path name
            path_name = str(item).split('/', maxsplit=10)[-1]
            if not "." in path_name and not "__" in path_name:
                # Obtain the intern paths for that
                paths = obtain_paths(str(item))
                # Just if you have paths, add them. If not, then ignore it
                if paths["Documentation"] or paths["Main files"]:
                    intern_paths[path_name] = paths
        if str(item).endswith(".py"):
            if "__init__.py" in str(item):
                intern_paths["Documentation"] = str(item)
            else:
                last_item = str(item).split('/', maxsplit=10)[-1]
                intern_paths["Main files"][last_item] = str(item)
    # Return the intern_paths
    return intern_paths


def gen_mkdocs_modules(paths: Dict[str, Union[list, dict, str]],
                       extra_tabs: int = 0) -> str:
    """Generate the MkDocs format from the given full paths obtained.
    Args:
    -----
        - paths (Dict[str, Union[list, dict, str]]): Paths to use to build automatically the docs.
        - folder (str): Folder that contains all the algorithms and files. Defaults to `modules`.
        - extra_tabs (int): It decides if we need to add extra tabs or not.
    """
    # Let's start the string.
    modules = "  - Home:  index.md\n  - Module Documentation:\n" if extra_tabs == 0 else ""
    # Now, from each path obtained over here, write the new modules section
    for module, sub_modules in paths.items():
        # For the first run
        if module == "Documentation":
            modules += f"    - Index: {sub_modules.replace('.py','.md')}\n"
            continue
        if module == "Main files":
            continue
        # For the next runs
        if sub_modules["Documentation"] or sub_modules["Main files"]:
            modules += "  "*extra_tabs+f"    - {prettify_text(module)}:\n"
            # Now, add the index for this sub_module if exists
            if sub_modules["Documentation"]:
                modules += "  "*extra_tabs + \
                    f"      - {sub_modules['Documentation'].replace('.py','.md')}\n"
            # If there's any file to add, then add it
            for file, file_path in sub_modules["Main files"].items():
                modules += "  "*extra_tabs + \
                    f"      - {prettify_text(file.replace('.py',''))}: {file_path.replace('.py','.md')}\n"
            # From here, remove main files and documentation from the sub_modules dict
            # but it do a copy so don't affect the real sub_modules dictionary
            copy_sub_modules = deepcopy(sub_modules)
            copy_sub_modules.pop("Main files")
            copy_sub_modules.pop("Documentation")
            # And iterate over these files and folders.
            if copy_sub_modules:
                modules += gen_mkdocs_modules(copy_sub_modules,
                                              extra_tabs=extra_tabs+1)
    # Return modules at the end
    return modules


def gen_pages(paths: Dict[str, Union[list, dict, str]]) -> None:
    """Generate a string with the classes, public methods, functions and other stuff that
    can be found on the given paths.
    Args:
    -------
        - paths (Dict[str, Union[list, dict, str]]): Paths to use to build automatically the docs.
    """
    for module, sub_modules in paths.items():
        # For the first run
        if module == "Documentation":
            # Generate the index for the entire page
            generate_md_files(sub_modules, index=True)
            continue
        if module == "Main files":
            continue
        # Now, add the index for this sub_module if exists
        if sub_modules["Documentation"]:
            # Generate the index for an specific module
            generate_md_files(sub_modules["Documentation"], index=True)
        # If there's any file to add, then add it
        for file_path in sub_modules["Main files"].values():
            generate_md_files(file_path)
        # From here, remove main files and documentation from the sub_modules dict
        # but it do a copy so don't affect the real sub_modules dictionary
        copy_sub_modules = deepcopy(sub_modules)
        copy_sub_modules.pop("Main files")
        copy_sub_modules.pop("Documentation")
        # And iterate over these files and folders with this same function
        if copy_sub_modules:
            gen_pages(copy_sub_modules)


def generate_md_files(file_path: str, index: bool = False) -> None:
    """From a given python file path, check if you can find any class or function (not private)
    that can be added to the documentation
    Args:
    -------
        - file_path (str): Python file path to check.
        - index (bool): Decides if this page to be created would be a index or not.
    """
    # To storage possible content
    if index:
        file_content: str = f"# **__{file_path.split('/',maxsplit=10)[-2].capitalize()}__**\n\n"
    else:
        file_content: str = f"# **__{prettify_text(file_path.split('/',maxsplit=10)[-1])}__**\n\n"
    # Open the python file
    with Path(file_path).open("r", encoding="utf-8") as python_file:
        all_lines = python_file.readlines()
        # Retrieve only those lines that start with "class", "def", "  def" or " def" since those
        # are the elements that we'd add on the string.
        useful_lines = list(filter(lambda line: line.startswith(
            ("class", "def", "  def", "    def")), all_lines))
        # If we have useful lines, then let check those
        if useful_lines:
            file_content += identify_type_of_code(file_path, useful_lines)
        elif index:
            # If this is a __init__, write what you expect to find here
            file_content += write_index_for_module(file_path)
        else:
            # If for some reason this file doesn't contains anything, then write a block that says
            # that we're working on it
            file_content += "!!! warning\n\tWe're working on this file. Please come back later!\n---\n"
    # At the end, create the file
    new_md_doc = Path("docs/"+file_path.replace(".py", ".md"))
    new_md_doc.parent.mkdir(parents=True, exist_ok=True)
    with new_md_doc.open("w", encoding="utf-8") as md_documentation:
        md_documentation.write(file_content)
    md_documentation.close()


def identify_type_of_code(file_path: str, file_lines: List[str]) -> str:
    """Identify the type of code and write what it needs based on if the code
    contains a class, a module with functions or something else.
    Args:
        file_path (str): Path of the file to open and review.
        file_lines (List[str]): Lines of the code to review.
    Returns:
        str: Code to write in the .md
    """
    file_content: str = ""  # Initialize the empty string
    # In case that we need to add options as methods, to just add the flag once
    options_already_added: bool = False
    path_to_use = file_path.replace("/", ".").replace(".py", "")
    for line in file_lines:
        if "class" in line:
            # Retrieve the name of the class with a regex expression
            search_class_name = re.search(r"class\W*(\w+)", line)
            # Obtain the class name from the search
            class_name = search_class_name.group(1)
            # Add this to the file that we're using
            file_content += f"::: {path_to_use}.{class_name}\n"
        else:
            # Retrieve the name of the class with a regex expression
            search_function_name = re.search(r"def\W*(\w+)", line)
            # Obtain the class name from the search
            function_name = search_function_name.group(1)
            # Also, just use this function (or method, if it is inside a class) it it's not private
            if function_name.startswith(("__", "_")):
                continue
            # Now, check if the startswith "  " or spaces. If it is, then it's a method of the class.
            if line.startswith(("\t", " ")):
                if not options_already_added:
                    options_already_added = True  # Avoid add this again
                    file_content += "    options:\n      members:\n"
                # Add the method to use
                file_content += f"        - {function_name}\n"
            else:
                # If not, it's a single function
                file_content += f"::: {path_to_use}.{function_name}\n"
    # Return whatever it had been found in the file
    return file_content


def write_index_for_module(file_path: str) -> str:
    """Write the index file for the different given modules
    Args:
        file_path (str): File path for search
    Returns:
        str: Content to write.
    """
    file_content: str = ""
    # Add some flags for the init module
    module_description: bool = False
    # Obtain not only the module folder, but also the init file
    index_file = Path(file_path)
    module_folder = index_file.parent
    with index_file.open("r", encoding="utf-8") as module_index:
        for line in module_index.readlines():
            if line.startswith("\"\"\""):
                # Remove or activate the flag for the module description
                module_description = module_description is False
                continue
            if line.startswith("from"):
                # Obtain the text that came after the import
                import_modules = line.split("import")[-1].split("\n")[0]
                # Just in case there's more than one import per line, split by commas
                modules = import_modules.split(",")
                # Add it to the file content
                for module in modules:
                    file_content += f"- [{module}]({module_folder}/{module})\n"
            # Add the add lines for the flags
            if module_description:
                file_content += line
    # If for some reason, the file content it's empty, then add a simple comment
    if not file_content:
        file_content += "!!! note\n\tModule documentation still to be written."
    # At the end, return the file content written
    return file_content


def generate_mk_document(repo: str, modules: str) -> None:
    """Generate the .yml for the `mkdocs.yml` or `mkgendocs.yml`
    depending on which it's the input given.
    Args:
    -------
        - repo(str): Name of the repository
        - modules(str): Modules to add(pages or the nav section)
    """
    # Start with the basic. Initialize the variable
    yml_file = f"site_name: {repo} API documentation\n"
    yml_file += f"repo_name: {repo}\nrepo_url: https://github.com/valiot/{repo}\n"
    yml_file += f"version: main\ncopyright: Copyright © 2018 - {date.now().year}, Valiot\n# Custom file now\n"
    # ---------------------------------------------------------------- #
    #                         CUSTOMIZATION                            #
    # ---------------------------------------------------------------- #
    # Now, customize the general visual with the theme and the custom dir, palette and color.
    yml_file += "theme:\n  name: 'material'\n  custom_dir: 'docs/overrides'\n  font:\n"
    yml_file += "    text: Fira Sans\n  palette:\n"
    # Add light and dark mode. First, go with the dark mode.
    yml_file += "    - scheme: slate\n      primary: 'teal'\n      accent: 'lime'\n      toggle:\n"
    yml_file += "        icon: material/toggle-switch\n        name: Switch to light mode\n"
    # Now, add the light mode
    yml_file += "    - scheme: default\n      primary: 'teal'\n      accent: 'lime'\n      toggle:\n"
    yml_file += "        icon: material/toggle-switch-off-outline\n        name: Switch to dark mode\n"
    # Now, add the logos
    yml_file += "  logo: 'assets/img/valiot-logo.png'\n  favicon: 'assets/img/valiot-icon.png'\n"
    # ---------------------------------------------------------------- #
    # Now, add the features
    yml_file += "  features:\n    - navigation.tabs\n    - navigation.tabs.sticky\n    - instant\n"
    # Add extensions
    yml_file += "markdown_extensions:\n  - admonition\n"
    # And, add the plugins
    yml_file += "plugins:\n  - search\n  - mkdocstrings\n  - section-index\n"
    # Add the coverage plugins
    yml_file += "  - coverage:\n      page_name: coverage\n      html_report_dir: htmlcov\n"
    # Add the slack button for help
    yml_file += "extra:\n  social:\n    - icon: fontawesome/brands/slack\n      "
    # The link to #valuechainos-pd
    yml_file += "link: https://valiot.slack.com/archives/C018WNQ3ALU\n"
    yml_file += "      name: If you have doubts, reach the team in the product channel."
    # Now, add the nav section and the modules
    yml_file += f"\nnav:\n{modules}\n"
    # Don't forget to add the development section
    yml_file += "  - Development:\n    - Coverage: coverage.md\n    - Code of conduct: CODE_OF_CONDUCT.md"
    # And save it
    with open("mkdocs.yml", "w", encoding="utf-8") as file:
        file.write(yml_file)
    file.close()


if __name__ == '__main__':
    # Obtain the values from the environment
    repo_folder = os.environ.get('REPO_MAIN_FOLDER')
    repo_name = os.environ.get("REPO")
    if not repo_folder:
        raise ValueError("We are not able to find the repo folder from where to extract the files." +
                         " Please ensure to add one with the environment variable name `REPO_MAIN_FOLDER`.")
    if not repo_name:
        raise ValueError("We are not able to find the repo name. Please ensure to add one with the" +
                         " environment variable name `REPO`.")
    # Remove the docs folder
    remove_docs_before_create(repo_folder)
    # Call the obtain paths
    full_paths = obtain_paths(repo_folder)
    # With the paths, generate the Markdown pages
    gen_pages(full_paths)
    # Now, create the MkDocs format
    mkdocs_modules = gen_mkdocs_modules(full_paths)
    # And, create the .yml files
    generate_mk_document(repo_name, mkdocs_modules)
