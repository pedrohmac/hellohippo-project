# Data processing project for Hello Hippo

This repository contains a simple solution to achieve the goals set for the data project.

## Features

This application accepts three directories to gather data from, and then writes three files in the `outputs` directory.

- **metrics_output.json**: Contains count of claims, reverds, average unit price and total price.
- **chain_recommendations.json**: The top two chains that offer lower prices per drug unit.
- **most_common_quantity.json**: The top 5 most common quantities prescribed for each drug.

### Improvements

The volume of data provided didn't required tools or frameworks other than Python and Pandas, in case of bigger volumes or streams of data there would be a need of databases to store processed metrics and aggregations, frameworks like Flink to process events and Airflow to schedule time series metric calculations.

### Prerequisites

    - Python
    - Pandas

### Steps

1. Install Dependencies

   Ensure you have Python and Pandas installed

2. Download datasets

   Download sample data (data.tar.gz) to the project root.

3. Run shell

   Run the shell script `entrypoint.sh` located in the project root.

   ```
   sh entrypoint.sh
   ```

4. Check resuts

   The results will be generated in the `outputs` directory located in the root directory.
