import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class LongMethodDetector {
    public static void main(String[] args) {
        BufferedReader reader;
        int lineCount = 0;
        int spaceCount = 0;
        int numberOfMethods = 0;

        try {
            reader = new BufferedReader(new FileReader("src/primitiva.py"));
            String line = reader.readLine();
            while (line != null) {
                if (isMethodStart(line)) {
                    if (lineCount > 10) {
                        System.out.println("Long method detected!!");
                    }

                    lineCount = 0;
                    numberOfMethods++;
                } else if(isMethodContent(line)) {
                    lineCount += spaceCount + 1;
                } else {
                    spaceCount++;
                }

                line = reader.readLine();
            }

            if (lineCount > 10) {
                System.out.println("Long method detected!!");
            }

            reader.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

        System.out.println("Number of methods = " + numberOfMethods);
    }

    private static boolean isMethodStart(String line) {
        String[] words = line.split(" ");
        return words[0].equals("def");
    }

    private static boolean isMethodContent(String line) {
        String[] words = line.split(" ");

        return words.length > 0;
    }
}
