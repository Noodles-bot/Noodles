import pyximport

pyximport.install()
import func


def main():
    """Gets info about bot"""
    python_files, cpp_files, total = func.info()
    print(f"Lines of Code: {total:,}\n")
    print(f'Number of Python files: {len(python_files)}\n')
    print(f'Number of C++ files: {len(cpp_files)}\n')


if __name__ == '__main__':
    main()
