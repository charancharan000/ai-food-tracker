import React, { useEffect, useRef } from "react";
import { View, Animated, StyleSheet, Easing } from "react-native";
import { Ionicons } from "@expo/vector-icons";

interface AnimatedTabIconProps {
  name: keyof typeof Ionicons.glyphMap;
  outlineName: keyof typeof Ionicons.glyphMap;
  focused: boolean;
  color: any;
  size?: number;
}

export const AnimatedTabIcon: React.FC<AnimatedTabIconProps> = ({
  name,
  outlineName,
  focused,
  color,
  size = 22,
}) => {
  const scaleAnim = useRef(new Animated.Value(focused ? 1.12 : 1.0)).current;
  const indicatorAnim = useRef(new Animated.Value(focused ? 1 : 0)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.timing(scaleAnim, {
        toValue: focused ? 1.12 : 1.0,
        duration: 180,
        easing: Easing.out(Easing.cubic),
        useNativeDriver: true,
      }),
      Animated.timing(indicatorAnim, {
        toValue: focused ? 1 : 0,
        duration: 180,
        easing: Easing.out(Easing.cubic),
        useNativeDriver: true,
      }),
    ]).start();
  }, [focused, scaleAnim, indicatorAnim]);

  return (
    <View style={styles.container}>
      <Animated.View style={{ transform: [{ scale: scaleAnim }] }}>
        <Ionicons
          name={focused ? name : outlineName}
          size={size}
          color={color}
        />
      </Animated.View>
      <Animated.View
        style={[
          styles.activeDot,
          {
            backgroundColor: color,
            opacity: indicatorAnim,
            transform: [{ scaleX: indicatorAnim }],
          },
        ]}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    alignItems: "center",
    justifyContent: "center",
    height: 32,
    width: 38,
  },
  activeDot: {
    width: 12,
    height: 2.5,
    borderRadius: 2,
    marginTop: 3,
  },
});
