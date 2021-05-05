from data import preprocess, scrape, postprocess

if __name__ == "__main__":
    globals()[sys.argv[1]]()
