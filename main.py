# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 11:02:06 2020

@author: OHyic

"""
#Import libraries
import os
import concurrent.futures
from GoogleImageScraper import GoogleImageScraper
from patch import webdriver_executable
import argparse

def worker_thread(search_key):
    image_scraper = GoogleImageScraper(
        webdriver_path, 
        output_dir, 
        search_key, 
        number_of_images, 
        headless, 
        min_resolution, 
        max_resolution, 
        max_missed)
    image_urls = image_scraper.find_image_urls()
    image_scraper.save_images(image_urls, keep_filenames)

    #Release resources
    del image_scraper

if __name__ == "__main__":
    #Define file path
    webdriver_path = os.path.normpath(os.path.join(os.getcwd(), 'webdriver', webdriver_executable()))
    # image_path = args.get("outputDir", os.path.normpath(os.path.join(os.getcwd(), 'photos')))

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Google Image Scraper")
    parser.add_argument("--nouns", type=str, help="Comma-separated list of search terms")
    parser.add_argument("--outputDir", type=str, help="Output directory for images")
    args = parser.parse_args()

    # if a nouns argument is passed, split it into a list by comma
    # 
    # if not, use the default list of search terms
    nouns = [noun.strip() for noun in args.nouns.split(",")] if args.nouns else ["cat", "t-shirt"]

    # parse output dir argument
    output_dir = args.outputDir if args.outputDir else os.path.normpath(os.path.join(os.getcwd(), 'photos'))

    search_keys = list(set(nouns))

    #Parameters
    number_of_images = 10                # Desired number of images
    headless = False                    # True = No Chrome GUI
    min_resolution = (600, 600)             # Minimum desired image resolution
    max_resolution = (9999, 9999)       # Maximum desired image resolution
    max_missed = 10                     # Max number of failed images before exit
    number_of_workers = 1               # Number of "workers" used
    keep_filenames = False              # Keep original URL image filenames

    #Run each search_key in a separate thread
    #Automatically waits for all threads to finish
    #Removes duplicate strings from search_keys
    with concurrent.futures.ThreadPoolExecutor(max_workers=number_of_workers) as executor:
        executor.map(worker_thread, search_keys)
