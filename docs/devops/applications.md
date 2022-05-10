# Just enough Applications

## Java

ssh app01 to login to app01 server and run below command to download

sudo curl https://download.java.net/java/GA/jdk13.0.2/d4173c853231432d94f001e99d882ca7/8/GPL/openjdk-13.0.2_linux-x64_bin.tar.gz --output /opt/openjdk-13.0.2_linux-x64_bin.tar.gz

To uncompress run sudo tar -xf /opt/openjdk-13.0.2_linux-x64_bin.tar.gz -C /opt/

To verify run /opt/jdk-13.0.2/bin/java -version on app01 and confirm correct version is installed


We need to set java binary path in environment PATH variable to use java binaries. So that you can simply run java instead of the full path.

Once done verify that you can invoke java simply by running java command.

Set path variable with the command export PATH=$PATH:/opt/jdk-13.0.2/bin

### Java Build & Packaging

1. Develop source code in `MyFile.java` file.
2. Compile with `javac MyFile.java` command.
3. Run with `java MyFile`

`jar cf MyApp.jar MyClass.class Service1.class Service2.class ...`

`java -jar MyApp.jar`

`javadoc -d doc MyClass.jar`

Build tools : Maven, Gradle, ANT

## NodeJS

`node -v`

`node add.js` pour lancer le script.

package manager : `npm` : Node Package Manager, npmjs.com.

`npm -v`

`npm search file`

`npm install file` local install, `npm install file -g` for global install.

`package.json` metadatas/dependencies of the package

`node -s "console.log(module.paths)"`

`ls /usr/lib/node_modules/npm/node_modules` builtin modules

`ls /usr/lib/node_modules`