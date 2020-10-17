import com.fasterxml.jackson.annotation.JsonProperty;
import com.google.gson.GsonBuilder;
import org.bson.types.ObjectId;

import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.*;

public class Reflections {

    private final Set<Class<?>> WRAPPER_TYPES = getWrapperTypes();

    public boolean isWrapperType(Class<?> clazz)
    {
        return WRAPPER_TYPES.contains(clazz);
    }

    public Object getDefaultValue(String key) {
        HashMap<String, Object> map = new HashMap<>();
        map.put("Integer", 1);
        map.put("Long", 1L);
        map.put("Byte", 1);
        map.put("Boolean", true);
        map.put("String", "String");
        map.put("ObjectId", new ObjectId().toHexString());
        map.put("LocalDate", LocalDate.of(2020, 10, 17).toString());
        map.put("BigDecimal", BigDecimal.ONE.toPlainString());
        return map.get(key);
    }

    public Class<?> getClassFromSimpleName(String key) {
        HashMap<String, Class<?>> map = new HashMap<>();
        map.put("String", String.class);
        map.put("Nested", SimpleInterface.Nested.class);
        return map.get(key);
    }

    private Set<Class<?>> getWrapperTypes()
    {
        Set<Class<?>> ret = new HashSet<>();
        ret.add(Boolean.class);
        ret.add(Character.class);
        ret.add(Byte.class);
        ret.add(Short.class);
        ret.add(Integer.class);
        ret.add(Long.class);
        ret.add(Float.class);
        ret.add(Double.class);
        ret.add(Void.class);
        ret.add(String.class);
        ret.add(ObjectId.class);
        ret.add(LocalDate.class);
        ret.add(BigDecimal.class);
        return ret;
    }

    public String getDefaultEnum(String key, Class<?> clazz) {
        HashMap<String, List<String>> map = new HashMap<>();
        map.put("SimpleEnum", Arrays.asList("Aditya", "Goldman"));

        for (Field f: clazz.getFields()) {
            System.out.println(f.getAnnotation(JsonProperty.class).value());
        }

        ArrayList<String> list = new ArrayList<>(map.get(key));
        Collections.shuffle(list);
        return list.get(0);
    }

    public static void main (String[] args) {
        HashMap<String, Object> m = new HashMap<>();
        m = new Reflections().go(m, SimpleInterface.class);
        System.out.println(new GsonBuilder().setPrettyPrinting().create().toJson(m));
    }

    public HashMap<String, Object> go(HashMap<String, Object> map, Class<?> c) {
        for (Method m: c.getMethods()) {
            if(m.getReturnType() != null && (m.getReturnType()).isEnum()) {
                map.put(m.getName(), getDefaultEnum(m.getReturnType().getSimpleName(), m.getReturnType()));
            } else if (m.getReturnType().equals(List.class)) {
                String simpleName = m.getAnnotation(ClassNameAnnotation.class).value();
                Class<?> listClass = getClassFromSimpleName(simpleName);
                if (!isWrapperType(listClass)) {
                    HashMap<String, Object> newMap = new HashMap<>();
                    newMap = go(newMap, listClass);
                    map.put(m.getName(), Arrays.asList(newMap));
                } else {
                    List<Object> newList = new ArrayList<>();
                    newList.add(getDefaultValue(simpleName));
                    map.put(m.getName(), newList);
                }
            } else if (!isWrapperType(m.getReturnType())) {
                HashMap<String, Object> newMap = new HashMap<>();
                newMap = go(newMap, m.getReturnType());
                map.put(m.getName(), newMap);
            } else {
                map.put(m.getName(), getDefaultValue(m.getReturnType().getSimpleName()));
            }
        }
        return map;
    }
}
