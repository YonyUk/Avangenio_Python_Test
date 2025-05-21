# <center>Proposed Solution</center>

## Required Implementations

> ### ***`tools`***  
Basic functions are defined for serializing, deserializing, and sending data through sockets.

> ### ***`protocol`***  

The communication protocol followed by both the client and server to exchange data is defined here.

> Characteristics:  

 - **`Structured communication`**: The classes ***`request`*** and ***`response`*** define how both sides communicate, providing a well-defined structure for these objects similar to ***`JavaScript Object Notation(json)`***, widely used globally. Both provide easy access to their members through dot notation (***`request`***.***`header`***), where ***`request`*** is an instance of the ***`request`*** class and ***`header`*** is a field of that instance. If the requested field does not exist, the returned value is ***`None`***.  
 - **`Well-defined operations`**: All permitted operations between the client and server are predefined within the ***`ServerOperation`*** class, which inherits from ***`enum`***, creating a collection of all possible operations.

## Client

### Visual Interface  
The ***`tkinter`*** library is used for a simple window as shown below:  

<center><img src="client_view.png" width="70%" height="70%"></center>

> ### Structure  
 - ***`configurable`***: Base implementation for creating easily configurable objects.  
 - ***`core`***: Implementations of necessary features for generating regulated strings and interacting with the ***`filesystem`***.  
 - ***`visual`***: Everything related to the client's visual interface, from the ***`AppConfig`*** class (used to configure the client application) to the ***`MainView`*** class, which handles the visual elements and the string generation process. The ***`App`*** class provides an additional abstraction for client windows and client initialization.  

### Configuration  
Client configuration is done through the ***`config.json`*** file located in the project root, which is read at the start of execution and passed as an initialization parameter to the application.  

Configurable parameters include:  
 - ***`host`***: Server address to which data will be sent.  
 - ***`port`***: Communication port between both parties.  
 - ***`pattern`***: Pattern for the generated strings, must be a text string representing a regular expression.  
 - ***`min_chars`***: Minimum number of characters allowed in the ***`Min. caracteres`*** input control.  
 - ***`max_chars`***: Maximum number of characters allowed in the ***`Max. caracteres`*** input control.  
 - ***`max_strings_by_process`***: Maximum number of strings generated per process during parallelization.  
 - ***`interface`***: Sub-configuration for the client's visual appearance.  
    - ***`size`***: Dimensions of the client's main window.  
    - ***`input_bg`***: Background color for the client's data entry fields.  
    - ***`input_fg`***: Font color for the client's data entry fields.  
    - ***`window`***: Sub-configuration for the client's main window; all applicable tkinter configurations for this component are valid.  
    - ***`input_controls`***: Sub-configuration for the client's input control containers; all applicable tkinter configurations for this component are valid.  
    - ***`buttons_controls`***: Sub-configuration for the client's buttons.  
        - ***`container`***: Sub-configuration for button containers; all applicable tkinter configurations are valid.  
        - ***`buttons`***: Sub-configuration for buttons; all applicable tkinter configurations are valid.  

### Functionality  
The client's visual interface captures the following values:  
 - ***`cantidad de cadenas`***: Number of strings to generate.  
 - ***`Min. caracteres`*** and ***`Max. caracteres`***: Minimum and maximum character lengths for the generated strings.  
 - ***`procesos por nucleo`***: Number of processes per core used during string generation to parallelize the process.  

When the ***`Generar fichero`*** button is pressed, a file with the specified strings is generated in a separate process to avoid freezing the interface. The generation is parallelized as follows:  
 - `1`: Compute the number of processes needed to generate the specified number of strings.  
 - `2`: Execute processes iteratively in batches of ***`procesos por nucleo`*** * ***`nucleos logicos`***.  
 - `3`: Each process, upon completion, locks the file to prevent race conditions, writes its generated strings, and then closes.  

If the application is closed during file generation, a confirmation dialog appears. If confirmed, the generation stops and changes are reverted. Pressing ***`Detener Generacion`*** stops generation and reverts changes.  

When the ***`Enviar fichero`*** button is pressed, the file is sent to the server for analysis, and a dialog displays the server's processing time.  

## Server  

### Structure  
Composed of two main components:  
 - ***`server`***: A minimalist ***`TCP`*** server implemented with ***`sockets`***, capable of integrating external service components to handle incoming requests.  
 - ***`service`***: A base service implementation and a functional service (***`WordPonderationService`***) specialized in handling requests from the aforementioned client.  

### Configuration  
Server and service configurations are located in the project root. Server configuration is in ***`config.json`***, while each service's configuration is in ***`<service>Config.json`***, where ***`<service>`*** is the service name added to the server.  

Configurable server parameters:  
 - ***`HOST`***: Server address.  
 - ***`PORT`***: Listening port for requests.  
 - ***`max_clients`***: Maximum simultaneous clients.  
 - ***`buffer_size`***: Bytes the server can read from the socket in a single attempt.  

Configurable parameters for ***`WordPonderationService`***:  
 - ***`special_pattern`***: Pattern excluded from the weighting function.  
 - ***`special_value`***: Value assigned to strings matching the defined pattern.  
 - ***`full_match`***: Determines if the pattern applies to the entire string or a section.  

Services without a configuration file use default parameters.  

### Weighting  
Similar to file generation on the client, weighting is performed in parallel across multiple processes. These processes coordinate to avoid race conditions when analyzing the file's words. Each process analyzes a subset of the words. 
