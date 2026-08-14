import java.io.IOException;
import java.util.HashMap;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class MatrixMultiplication {

  public static class MatrixMapper extends Mapper<Object, Text, Text, Text> {
    public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
      Configuration conf = context.getConfiguration();
      int m = Integer.parseInt(conf.get("m"));
      int p = Integer.parseInt(conf.get("p"));
      
      String line = value.toString();
      String[] indicesAndValue = line.split(",");
      Text outputKey = new Text();
      Text outputValue = new Text();
      
      // Matrix A input format: A,i,j,value (i=row, j=col)
      if (indicesAndValue[0].equals("A")) {
        int i = Integer.parseInt(indicesAndValue[1]);
        String j = indicesAndValue[2];
        String a_ij = indicesAndValue[3];
        // Emit for each column of output matrix C
        for (int k = 0; k < p; k++) {
          outputKey.set(i + "," + k);
          outputValue.set("A," + j + "," + a_ij);
          context.write(outputKey, outputValue);
        }
      } 
      // Matrix B input format: B,j,k,value (j=row, k=col)
      else if (indicesAndValue[0].equals("B")) {
        String j = indicesAndValue[1];
        int k = Integer.parseInt(indicesAndValue[2]);
        String b_jk = indicesAndValue[3];
        // Emit for each row of output matrix C
        for (int i = 0; i < m; i++) {
          outputKey.set(i + "," + k);
          outputValue.set("B," + j + "," + b_jk);
          context.write(outputKey, outputValue);
        }
      }
    }
  }

  public static class MatrixReducer extends Reducer<Text, Text, Text, Text> {
    public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
      String[] value;
      // Use j as the key for HashMaps to match A's columns and B's rows
      HashMap<Integer, Float> hashA = new HashMap<Integer, Float>();
      HashMap<Integer, Float> hashB = new HashMap<Integer, Float>();
      
      for (Text val : values) {
        value = val.toString().split(",");
        if (value[0].equals("A")) {
          hashA.put(Integer.parseInt(value[1]), Float.parseFloat(value[2]));
        } else {
          hashB.put(Integer.parseInt(value[1]), Float.parseFloat(value[2]));
        }
      }
      
      int n = Integer.parseInt(context.getConfiguration().get("n"));
      float result = 0.0f;
      
      // C(i,k) = sum over j (A(i,j) * B(j,k))
      for (int j = 0; j < n; j++) {
        float a_ij = hashA.containsKey(j) ? hashA.get(j) : 0.0f;
        float b_jk = hashB.containsKey(j) ? hashB.get(j) : 0.0f;
        result += a_ij * b_jk;
      }
      
      // Output format: i,k,value
      if (result != 0.0f) {
        context.write(null, new Text(key.toString() + "," + Float.toString(result)));
      }
    }
  }

  public static void main(String[] args) throws Exception {
    if (args.length != 5) {
      System.err.println("Usage: MatrixMultiplication <in_dir> <out_dir> <m> <n> <p>");
      System.err.println("m: rows of matrix A, n: cols of A (which is rows of B), p: cols of matrix B");
      System.exit(2);
    }
    
    Configuration conf = new Configuration();
    // Pass matrix dimensions to mapper and reducer via configuration
    conf.set("m", args[2]);
    conf.set("n", args[3]);
    conf.set("p", args[4]);
    
    Job job = Job.getInstance(conf, "Matrix Multiplication");
    job.setJarByClass(MatrixMultiplication.class);
    
    job.setMapperClass(MatrixMapper.class);
    job.setReducerClass(MatrixReducer.class);
    
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(Text.class);
    
    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));
    
    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}
