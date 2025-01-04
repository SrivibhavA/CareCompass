import React, { useState } from 'react';
import { 
  StyleSheet, 
  Text, 
  View, 
  TouchableOpacity, 
  TextInput, 
  ScrollView, 
  SafeAreaView,
  Image 
} from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { Mic, Eye } from 'lucide-react-native';

const Stack = createStackNavigator();

// Welcome Screen
const WelcomeScreen = ({ navigation }) => {
  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.logo}>CareCompass</Text>
        <Image source={require('./assets/compass-icon.png')} style={styles.compassIcon} />
      </View>
      
      <Image 
        source={require('./assets/doctor-patient.jpg')} 
        style={styles.welcomeImage}
      />
      
      <TouchableOpacity 
        style={styles.button}
        onPress={() => navigation.navigate('Home')}
      >
        <Text style={styles.buttonText}>Get Started</Text>
      </TouchableOpacity>
      
      <TouchableOpacity onPress={() => navigation.navigate('Login')}>
        <Text style={styles.linkText}>Already have an account? Log In...</Text>
      </TouchableOpacity>
    </View>
  );
};

// Home Screen
const HomeScreen = ({ navigation }) => {
  return (
    <View style={styles.container}>
      <Text style={styles.welcomeBack}>Welcome Back!</Text>
      
      <TouchableOpacity 
        style={styles.button}
        onPress={() => navigation.navigate('AddEntry')}
      >
        <Text style={styles.buttonText}>Add journal entry...</Text>
      </TouchableOpacity>
      
      <TouchableOpacity 
        style={styles.button}
        onPress={() => navigation.navigate('PreviousEntries')}
      >
        <Text style={styles.buttonText}>Your previous Journal Entries...</Text>
      </TouchableOpacity>
      
      <TouchableOpacity style={styles.button}>
        <Text style={styles.buttonText}>More Options...</Text>
      </TouchableOpacity>
      
      <TouchableOpacity style={styles.button}>
        <Text style={styles.buttonText}>Contact Doctor</Text>
      </TouchableOpacity>
      
      <Text style={styles.emergencyText}>
        If this is an emergency, call 911
      </Text>
    </View>
  );
};

// Add Entry Screen
const AddEntryScreen = () => {
  const [selectedMood, setSelectedMood] = useState(null);
  
  const moods = [
    { value: 1, color: '#FF4D4D' },
    { value: 2, color: '#FFA07A' },
    { value: 3, color: '#FFD700' },
    { value: 4, color: '#90EE90' },
    { value: 5, color: '#32CD32' },
  ];

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Add a Journal Entry</Text>
      
      <View style={styles.inputContainer}>
        <TextInput
          style={styles.textInput}
          placeholder="Add text here..."
          multiline
          numberOfLines={6}
        />
        <Mic style={styles.micIcon} />
      </View>
      
      <Text style={styles.feelingText}>How do you feel?</Text>
      <View style={styles.moodContainer}>
        {moods.map((mood, index) => (
          <TouchableOpacity
            key={index}
            style={[
              styles.moodButton,
              { backgroundColor: mood.color },
              selectedMood === mood.value && styles.selectedMood
            ]}
            onPress={() => setSelectedMood(mood.value)}
          />
        ))}
      </View>
      
      <TouchableOpacity style={styles.button}>
        <Text style={styles.buttonText}>Done!</Text>
      </TouchableOpacity>
    </View>
  );
};

// Previous Entries Screen
const PreviousEntriesScreen = () => {
  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>Your previous Journal Entries</Text>
      
      {[1, 2, 3, 4, 5].map((entry) => (
        <View key={entry} style={styles.entryCard}>
          <View style={styles.entryInfo}>
            <Text style={styles.entryLabel}>Date Written:</Text>
            <Text style={styles.entryLabel}>Your Feeling:</Text>
            <Text style={styles.entryLabel}>Doctor's Comment:</Text>
          </View>
          
          <View style={styles.entrySeparator} />
          
          <View style={styles.entryContent}>
            <Text style={styles.entryTitle}>Journal Entry:</Text>
            <Eye style={styles.eyeIcon} />
          </View>
        </View>
      ))}
    </ScrollView>
  );
};

// App Component
export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Welcome">
        <Stack.Screen 
          name="Welcome" 
          component={WelcomeScreen}
          options={{ headerShown: false }}
        />
        <Stack.Screen 
          name="Home" 
          component={HomeScreen}
          options={{ headerShown: false }}
        />
        <Stack.Screen 
          name="AddEntry" 
          component={AddEntryScreen}
          options={{ headerShown: false }}
        />
        <Stack.Screen 
          name="PreviousEntries" 
          component={PreviousEntriesScreen}
          options={{ headerShown: false }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#00CED1',
    padding: 20,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 20,
  },
  logo: {
    fontSize: 24,
    fontWeight: 'bold',
    color: 'white',
  },
  compassIcon: {
    width: 30,
    height: 30,
    marginLeft: 10,
  },
  welcomeImage: {
    width: '100%',
    height: 300,
    borderRadius: 20,
    marginBottom: 30,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: 'white',
    marginBottom: 20,
  },
  welcomeBack: {
    fontSize: 32,
    fontWeight: 'bold',
    color: 'white',
    marginBottom: 40,
    textAlign: 'center',
  },
  button: {
    backgroundColor: 'white',
    padding: 15,
    borderRadius: 25,
    marginVertical: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  buttonText: {
    color: '#00CED1',
    fontSize: 18,
    textAlign: 'center',
  },
  linkText: {
    color: 'white',
    fontSize: 16,
    textAlign: 'center',
    marginTop: 20,
  },
  emergencyText: {
    color: 'white',
    fontSize: 18,
    textAlign: 'center',
    marginTop: 40,
  },
  inputContainer: {
    backgroundColor: 'white',
    borderRadius: 25,
    padding: 15,
    marginBottom: 20,
  },
  textInput: {
    height: 150,
    textAlignVertical: 'top',
  },
  micIcon: {
    position: 'absolute',
    bottom: 15,
    right: 15,
  },
  feelingText: {
    fontSize: 24,
    color: 'white',
    textAlign: 'center',
    marginVertical: 20,
  },
  moodContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginBottom: 30,
  },
  moodButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
  },
  selectedMood: {
    borderWidth: 3,
    borderColor: 'white',
  },
  entryCard: {
    backgroundColor: 'white',
    borderRadius: 25,
    padding: 15,
    marginBottom: 15,
    flexDirection: 'row',
  },
  entryInfo: {
    flex: 1,
  },
  entrySeparator: {
    width: 2,
    backgroundColor: '#00CED1',
    marginHorizontal: 15,
  },
  entryContent: {
    flex: 1,
    alignItems: 'center',
  },
  entryLabel: {
    color: '#00CED1',
    marginVertical: 5,
  },
  entryTitle: {
    color: '#00CED1',
    fontWeight: 'bold',
    marginBottom: 10,
  },
});