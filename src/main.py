import argparse
import sys
from imdbClassDataSet import ImdbDataSet

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--type_', type=str, default='movie', help='Elige el tipo de contenido')
    parser.add_argument('--genre', type=str, default='comedy', help='Elige el tipo de genero del contenido')

    args = parser.parse_args()

    scraper = ImdbDataSet(args.type_, args.genre)
    scraper(200)
    scraper.save_dataset()

if __name__=='__main__':
    main()




