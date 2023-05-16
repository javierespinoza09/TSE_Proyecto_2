from datetime import datetime
start_time=None

# Start the stopwatch
start_time = datetime.now()

# Wait for a keyboard interrupt (CTRL+C) to stop the stopwatch
while True:
    with open("registros.txt", "a") as f:
        f.write(f"{start_time}\n")

    file_path = "Desktop/settings.txt"
    try:
        with open(file_path, "r") as file:
            file_contents = file.readlines()

            if len(file_contents) >= 2:
                # Extract the "Off" string
                keyword = "On/Off: "
                off_string = file_contents[1].strip().split(keyword)[1]
                print(off_string)  # Output: Off
            else:
                print("Invalid file format: Insufficient lines in the file.")
    except FileNotFoundError:
        print("File not found.")
    
    if off_string=="Off":
        end_time = datetime.now()

        # Calculate the elapsed time
        elapsed_time = end_time - start_time

        # Print the elapsed time
        print("Elapsed time: {}".format(elapsed_time))
        with open("registros.txt", "a") as f:
            f.write(f"End time: {end_time}, Start time: {start_time}, Elapsed time: {elapsed_time}\n")


        break
    else:
        pass