// Generated by gencpp from file adeept_awr_ros_driver/ArrayIR.msg
// DO NOT EDIT!


#ifndef ADEEPT_AWR_ROS_DRIVER_MESSAGE_ARRAYIR_H
#define ADEEPT_AWR_ROS_DRIVER_MESSAGE_ARRAYIR_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>

#include <std_msgs/Header.h>

namespace adeept_awr_ros_driver
{
template <class ContainerAllocator>
struct ArrayIR_
{
  typedef ArrayIR_<ContainerAllocator> Type;

  ArrayIR_()
    : header()
    , left(false)
    , middle(false)
    , right(false)  {
    }
  ArrayIR_(const ContainerAllocator& _alloc)
    : header(_alloc)
    , left(false)
    , middle(false)
    , right(false)  {
  (void)_alloc;
    }



   typedef  ::std_msgs::Header_<ContainerAllocator>  _header_type;
  _header_type header;

   typedef uint8_t _left_type;
  _left_type left;

   typedef uint8_t _middle_type;
  _middle_type middle;

   typedef uint8_t _right_type;
  _right_type right;





  typedef boost::shared_ptr< ::adeept_awr_ros_driver::ArrayIR_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::adeept_awr_ros_driver::ArrayIR_<ContainerAllocator> const> ConstPtr;

}; // struct ArrayIR_

typedef ::adeept_awr_ros_driver::ArrayIR_<std::allocator<void> > ArrayIR;

typedef boost::shared_ptr< ::adeept_awr_ros_driver::ArrayIR > ArrayIRPtr;
typedef boost::shared_ptr< ::adeept_awr_ros_driver::ArrayIR const> ArrayIRConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::adeept_awr_ros_driver::ArrayIR_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::adeept_awr_ros_driver::ArrayIR_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace adeept_awr_ros_driver

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': False, 'IsMessage': True, 'HasHeader': True}
// {'std_msgs': ['/opt/ros/melodic/share/std_msgs/cmake/../msg'], 'adeept_awr_ros_driver': ['/home/pham/enph353_ws/src/2019F_competition_students/adeept_awr_ros_driver/msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::adeept_awr_ros_driver::ArrayIR_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::adeept_awr_ros_driver::ArrayIR_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct IsMessage< ::adeept_awr_ros_driver::ArrayIR_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::adeept_awr_ros_driver::ArrayIR_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::adeept_awr_ros_driver::ArrayIR_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::adeept_awr_ros_driver::ArrayIR_<ContainerAllocator> const>
  : TrueType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::adeept_awr_ros_driver::ArrayIR_<ContainerAllocator> >
{
  static const char* value()
  {
    return "232d72af632e962eb66f18154418a761";
  }

  static const char* value(const ::adeept_awr_ros_driver::ArrayIR_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x232d72af632e962eULL;
  static const uint64_t static_value2 = 0xb66f18154418a761ULL;
};

template<class ContainerAllocator>
struct DataType< ::adeept_awr_ros_driver::ArrayIR_<ContainerAllocator> >
{
  static const char* value()
  {
    return "adeept_awr_ros_driver/ArrayIR";
  }

  static const char* value(const ::adeept_awr_ros_driver::ArrayIR_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::adeept_awr_ros_driver::ArrayIR_<ContainerAllocator> >
{
  static const char* value()
  {
    return "Header header\n"
"bool left\n"
"bool middle\n"
"bool right\n"
"\n"
"================================================================================\n"
"MSG: std_msgs/Header\n"
"# Standard metadata for higher-level stamped data types.\n"
"# This is generally used to communicate timestamped data \n"
"# in a particular coordinate frame.\n"
"# \n"
"# sequence ID: consecutively increasing ID \n"
"uint32 seq\n"
"#Two-integer timestamp that is expressed as:\n"
"# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')\n"
"# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')\n"
"# time-handling sugar is provided by the client library\n"
"time stamp\n"
"#Frame this data is associated with\n"
"string frame_id\n"
;
  }

  static const char* value(const ::adeept_awr_ros_driver::ArrayIR_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::adeept_awr_ros_driver::ArrayIR_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.header);
      stream.next(m.left);
      stream.next(m.middle);
      stream.next(m.right);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct ArrayIR_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::adeept_awr_ros_driver::ArrayIR_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::adeept_awr_ros_driver::ArrayIR_<ContainerAllocator>& v)
  {
    s << indent << "header: ";
    s << std::endl;
    Printer< ::std_msgs::Header_<ContainerAllocator> >::stream(s, indent + "  ", v.header);
    s << indent << "left: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.left);
    s << indent << "middle: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.middle);
    s << indent << "right: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.right);
  }
};

} // namespace message_operations
} // namespace ros

#endif // ADEEPT_AWR_ROS_DRIVER_MESSAGE_ARRAYIR_H