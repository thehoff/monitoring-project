#!/usr/bin/python

from socket import gethostname

#Datastructure
class ExportData(object):
    """
    This datastructure holds all data needed for an output routine.
    Data will be serialized from this datastructure as it is exported
    by different output modules for each data receiver (influxdb, logstash,
    http, etc.)

    | data_set_name |   {fixed_tags}    | {variable_tags}      |   {data}   |

    example:
    | "iface_state" | {"host":"leaf01"} | {"interface":"eth0"} | {"linkstate":"up"} |

    """

    def __init__(self, data_set_name, fixed_tags=None, variable_tags=None, data=None):
        self.data_set_name = str(data_set_name)

        # fixed_tags can optionally be provided in a dict upong DS declaration
        if fixed_tags==None:
            self.fixed_tags={'host':gethostname()}
        elif type(fixed_tags) is dict:
            self.fixed_tags = fixed_tags
            self.fixed_tags['host']=gethostname()
        else:
            print "ERROR: if passing fixed_tags, type must be a dict!"
            exit(1)

        # variable_tags can optionally be provided in a dict upong DS declaration
        if variable_tags==None:
            self.variable_tags = []
            if data != None: self.variable_tags.append({})
        elif type(variable_tags) is dict:
            self.variable_tags = [variable_tags]
        else:
            print "ERROR: if passing variable_tags, type must be a dict!"
            exit(1)

        # data can optionally be provided in a dict upon DS declaration
        if data==None:
            self.data = []
            if variable_tags != None: self.data.append({})
        elif type(data) is dict:
            self.data = [data]
        else:
            print "ERROR: if passing data, type must be a dict!"
            exit(1)

    def show_data(self):
        """
        Used for debugging purposes, this function displays data in a human readable format.
        """
        output = "######################\n"
        output+= "   Sanity checking:\n"
        output+= "######################\n"
        output+= "<data set name is: %s >\n" % self.data_set_name
        output+= "    data has fixed tags: \n        "
        output+= "%s \n" % (self.__fixed_tags())
        output+= "    variable_tags     data\n"
        for i in range(0,len(self.data)):
            output += "      %s    %s\n" % (self.__variable_tags(i),self.__data_points(i)[0:-1])
        print output

    def add_row(self,variable_tags,data):
        if type(data) is not dict:
            print "ERROR: Data must be provided in Dictionary!"
            exit(1)
        self.data.append(data)

        if type(variable_tags) is not dict:
            print "ERROR: if passing variable_tags, type must be a dict!"
            exit(1)
        self.variable_tags.append(variable_tags)


    def send_data(self,recipients):
        """
        This function defines which targets will receive the data.
        """
        targets = recipients.split(',')
        for target in targets:
            if target == "cli": print self
            else:
                print "ERROR: Method %s not implemented!" % target
                exit(1)

    def __fixed_tags(self):
        fixed_tags_string=""
        for tag in self.fixed_tags:
            fixed_tags_string+= "%s=%s" % (tag,self.fixed_tags[tag])
        return fixed_tags_string

    def __variable_tags(self,index):
        variable_tags_string=""
        for tag in self.variable_tags[index]:
            variable_tags_string+= ",%s=%s" % (tag,self.variable_tags[index][tag])
        if variable_tags_string == "":
            return ""
        return variable_tags_string

    def __data_points(self,index):
        data_points_string=""
        data_element = self.data[index]
        for data_column in data_element:
            data_points_string += "%s=%s," % (data_column,data_element[data_column])
        if data_points_string == "":
            return ""
        return data_points_string[0:-1]

    def __repr__(self):
        output=""
        for i in range(0,len(self.data)):
            output += "%s,%s%s %s\n" % (self.data_set_name,self.__fixed_tags(),self.__variable_tags(i),self.__data_points(i))
        return output
