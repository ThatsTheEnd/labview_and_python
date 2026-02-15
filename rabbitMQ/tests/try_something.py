from concurrent.futures import ThreadPoolExecutor, as_completed
import time


def work(name: str, seconds: float) -> str:
    time.sleep(seconds)    
    return f"{name} done"


def main() -> None:
    jobs = [("CH1", 1.5), ("CH2", 2.5), ("CH3", 1.0)]

    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = [pool.submit(work, ch, t) for ch, t in jobs]

        for f in as_completed(futures): 
            print(f.result())


if __name__ == "__main__":
    main()


