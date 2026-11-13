import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaPairRDD;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import scala.Tuple2;

import java.io.Serializable;
import java.util.List;

/**
 * Question 6: Find the Maximum Temperature using Apache Spark (Java API)
 *
 * Big Data Analytics Lab Program
 *
 * Description:
 * Reads weather sensor / NCDC records, extracts (Year, Temperature) pairs,
 * filters invalid/missing sensor data (such as 9999 or corrupt lines),
 * and computes the maximum temperature recorded for each year using reduceByKey.
 * Finally, it computes and displays the overall highest temperature recorded across all years.
 */
public class MaxTemperature implements Serializable {

    public static void main(String[] args) {
        // Path to input file (defaults to temperatures.txt in the current directory)
        String inputPath = (args.length > 0) ? args[0] : "temperatures.txt";

        // 1. Initialize Spark Configuration and JavaSparkContext
        SparkConf conf = new SparkConf()
                .setAppName("MaxTemperatureJavaSpark")
                .setMaster("local[*]"); // Use all local CPU cores
        JavaSparkContext sc = new JavaSparkContext(conf);
        sc.setLogLevel("WARN"); // Reduce verbose Spark INFO logging

        System.out.println("===============================================================================");
        System.out.println("       BIG DATA ANALYTICS: MAXIMUM TEMPERATURE FINDER USING SPARK (JAVA)       ");
        System.out.println("===============================================================================");
        System.out.println("Loading input file from: " + inputPath);

        // 2. Load input file into an RDD of Strings
        JavaRDD<String> rawLines = sc.textFile(inputPath);

        // 3. Filter comments / headers and empty lines, then parse (Year, Temperature)
        JavaPairRDD<String, Double> validYearTemps = rawLines
                .filter(line -> line != null && !line.trim().isEmpty() && !line.startsWith("#") && !line.toLowerCase().startsWith("year"))
                .flatMapToPair(line -> {
                    String clean = line.trim();
                    try {
                        String year;
                        double temp;

                        if (clean.contains(",")) {
                            // Standard CSV Format: Year,Temperature
                            String[] parts = clean.split(",");
                            year = parts[0].trim();
                            temp = Double.parseDouble(parts[1].trim());
                        } else if (clean.length() >= 92 && Character.isDigit(clean.charAt(15))) {
                            // Official NCDC Fixed-Width Format:
                            // Year is characters 15-19, Temperature is characters 87-92 (scaled by 10)
                            year = clean.substring(15, 19);
                            int tempInt = Integer.parseInt(clean.substring(87, 92));
                            temp = tempInt / 10.0;
                        } else {
                            // Space/Tab-delimited format
                            String[] parts = clean.split("\\s+");
                            year = parts[0].trim();
                            temp = Double.parseDouble(parts[parts.length - 1].trim());
                        }

                        // Filter out sentinel/missing values: 9999.0, 999.9, etc.
                        if (temp > -100.0 && temp < 100.0 && temp != 999.9 && temp != 9999.0) {
                            return List.of(new Tuple2<>(year, temp)).iterator();
                        }
                    } catch (Exception ignored) {
                        // Skip malformed lines
                    }
                    return List.<Tuple2<String, Double>>of().iterator();
                });

        // 4. Reduce by Year to find Maximum Temperature per Year
        JavaPairRDD<String, Double> maxTempByYear = validYearTemps
                .reduceByKey(Math::max)
                .sortByKey(true); // Sort chronologically by year

        // 5. Collect and display results
        List<Tuple2<String, Double>> results = maxTempByYear.collect();

        System.out.println("===============================================================================");
        System.out.printf("%-15s | %-25s%n", "Year", "Max Recorded Temp (°C)");
        System.out.println("-------------------------------------------------------------------------------");

        Tuple2<String, Double> globalMax = null;

        for (Tuple2<String, Double> entry : results) {
            System.out.printf("%-15s | %-25.2f%n", entry._1(), entry._2());
            if (globalMax == null || entry._2() > globalMax._2()) {
                globalMax = entry;
            }
        }

        System.out.println("===============================================================================");
        if (globalMax != null) {
            System.out.printf("OVERALL MAXIMUM TEMPERATURE RECORDED: %.2f °C in Year %s%n", globalMax._2(), globalMax._1());
        } else {
            System.out.println("No valid temperature records found.");
        }
        System.out.println("===============================================================================");

        // 6. Stop Spark Context
        sc.stop();
    }
}
