import java.io.IOException;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class MovieTags {

  public static class TagMapper extends Mapper<Object, Text, Text, Text> {
    private Text outKey = new Text();
    private Text outValue = new Text();

    public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
      String line = value.toString();
      
      // Skip the CSV header line
      if (line.startsWith("userId") || line.startsWith("userId,movieId")) {
        return;
      }
      
      // MovieLens tags.csv format: userId,movieId,tag,timestamp
      String[] parts = line.split(",", 4); 
      
      if (parts.length >= 3) {
        String movieId = parts[1].trim();
        String tag = parts[2].trim();
        
        outKey.set(movieId);
        outValue.set(tag);
        context.write(outKey, outValue);
      }
    }
  }

  public static class TagReducer extends Reducer<Text, Text, Text, Text> {
    private Text result = new Text();

    public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
      StringBuilder tagsList = new StringBuilder();
      boolean first = true;
      
      // Combine all tags for this movieId into a separated list
      for (Text val : values) {
        if (!first) {
          tagsList.append(" | ");
        }
        tagsList.append(val.toString());
        first = false;
      }
      
      result.set(tagsList.toString());
      context.write(key, result);
    }
  }

  public static void main(String[] args) throws Exception {
    if (args.length != 2) {
      System.err.println("Usage: MovieTags <input path> <output path>");
      System.exit(-1);
    }
    
    Configuration conf = new Configuration();
    Job job = Job.getInstance(conf, "movie tags");
    job.setJarByClass(MovieTags.class);
    
    job.setMapperClass(TagMapper.class);
    job.setReducerClass(TagReducer.class);
    
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(Text.class);
    
    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));
    
    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}
