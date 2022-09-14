#ifndef _VELODYNE_PLUGIN_HH_
#define _VELODYNE_PLUGIN_HH_

#include <gazebo/gazebo.hh>
#include <gazebo/physics/physics.hh>

#include <gazebo/common/Plugin.hh>
#include "ros/ros.h"
#include "ros/callback_queue.h"
#include "ros/subscribe_options.h"
#include <std_msgs/String.h>

namespace gazebo
{
    /// \brief A plugin to control a Velodyne sensor.
    class OjosPlugin : public ModelPlugin
    {
        /// \brief Constructor
    public:
        OjosPlugin()
        {
            printf("Hello World!\n");
        }
    private: std::unique_ptr<ros::NodeHandle> rosNode;
    private: ros::Publisher rosPub;
    private: ros::CallbackQueue rosQueue;
    private: std::thread rosQueueThread;
        /// \brief The load function is called by Gazebo when the plugin is
        /// inserted into simulation
        /// \param[in] _model A pointer to the model that this plugin is
        /// attached to.
        /// \param[in] _sdf A pointer to the plugin's SDF element.
    public:
        virtual void Load(physics::ModelPtr _model, sdf::ElementPtr _sdf)
        {
            // Safety check
            if (_model->GetJointCount() == 0)
            {
                std::cerr << "Invalid joint count, Velodyne plugin not loaded\n";
                return;
            }
            printf(_model->GetJointCount() + "\n");
            //for each joint in the model, get the name and print it
            for (physics::Joint_V::const_iterator j = _model->GetJoints().begin(); j != _model->GetJoints().end(); ++j)
            {
                printf((((*j)->GetName())+"\n").c_str());
            }
            //leftPlate
            physics::JointPtr joint = _model->GetJoint("leftPlate");
        
        }
    };

    // Tell Gazebo about this plugin, so that Gazebo can call Load on this plugin.
    GZ_REGISTER_MODEL_PLUGIN(OjosPlugin)
}
#endif