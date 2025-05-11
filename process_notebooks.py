import os
import json
import shutil
from pathlib import Path

def process_notebooks(directory_path, dry_run=False):
    """
    Process all Jupyter notebooks in the given directory that don't already have 'cb' appended.
    
    Args:
        directory_path (str): Path to the directory containing notebooks
        dry_run (bool): If True, only print what would be done without actually doing it
    """
    directory = Path(directory_path)
    
    # Find all .ipynb files that don't end with cb.ipynb
    notebook_files = [f for f in directory.glob('*.ipynb') 
                     if not f.stem.endswith('_cb')]
    
    if not notebook_files:
        print("No notebooks found to process.")
        return
    
    processed_count = 0
    
    for notebook_file in notebook_files:
        try:
            print(f"\nProcessing: {notebook_file.name}")
            
            # Create the new filename
            new_name = notebook_file.stem + '_cb.ipynb'
            new_path = notebook_file.parent / new_name
            
            # Check if the cb version already exists
            if new_path.exists():
                print(f"  - Skipping: {new_name} already exists")
                continue
            
            if dry_run:
                print(f"  - Would create: {new_name}")
                continue
            
            # Read the notebook
            with open(notebook_file, 'r', encoding='utf-8') as f:
                notebook = json.load(f)
            
            # Process cells
            for cell in notebook['cells']:
                if cell['cell_type'] == 'code':
                    # Clear the code content but keep the empty cell
                    cell['source'] = []
                    # Clear outputs
                    cell['outputs'] = []
                    if 'execution_count' in cell:
                        cell['execution_count'] = None
                # Markdown cells are left unchanged
            
            # Write the new notebook
            with open(new_path, 'w', encoding='utf-8') as f:
                json.dump(notebook, f, indent=1, ensure_ascii=False)
            
            print(f"  - Created: {new_name}")
            processed_count += 1
            
        except Exception as e:
            print(f"  - Error processing {notebook_file.name}: {str(e)}")
    
    print(f"\nProcessed {processed_count} notebook(s) successfully.")


def main():
    """Main function with command-line argument handling"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Create codebook versions of Jupyter notebooks')
    parser.add_argument('directory', 
                       nargs='?', 
                       default='.', 
                       help='Directory containing notebooks (default: current directory)')
    parser.add_argument('--dry-run', 
                       action='store_true', 
                       help='Show what would be done without actually doing it')
    
    args = parser.parse_args()
    
    # Verify the directory exists
    if not os.path.isdir(args.directory):
        print(f"Error: '{args.directory}' is not a valid directory")
        return 1
    
    print(f"Processing notebooks in: {args.directory}")
    if args.dry_run:
        print("(DRY RUN - no changes will be made)")
    
    process_notebooks(args.directory, args.dry_run)
    
    return 0


if __name__ == "__main__":
    exit(main())