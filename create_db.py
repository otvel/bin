import gzip

print("Starting Download")

with open("perhoset.fa", "w") as outfh:
    with open("download_links.txt") as infh:
        for line in infh:
            link = line.strip()
            print(f"Downloading {link}")
            with gzip.open(urlopen(link)) as linkfh:
                for line in linkfh:
                    try:
                        line = line.decode("utf-8")
                    except Exception as e:
                        print(e)
                        print("Ignoring utf-8 errors")
                        line = line.decode("utf-8", "ignore")
                    outfh.write(line)

print("Done!")
