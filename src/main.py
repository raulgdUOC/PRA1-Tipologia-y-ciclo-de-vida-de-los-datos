import argparse
import sys
from imdbClassDataSet import ImdbDataSet

def main():
    # Catching the data wrote in console
    parser = argparse.ArgumentParser()
    parser.add_argument('--type_', type=str, default='movie', help='Elige el tipo de contenido')
    parser.add_argument('--genre', type=str, default='comedy', help='Elige el tipo de genero del contenido')

    args = parser.parse_args()

    # Data is collected through ImdbDataSet
    scraper = ImdbDataSet(type_=args.type_, genre=args.genre)  # Instantiate the class
    scraper(200)  # Getting the information from the first 200 pages
    scraper.save_dataset()  # Saving the dataset


if __name__ == '__main__':
    main()
    
