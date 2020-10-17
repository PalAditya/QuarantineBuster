import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import java.lang.reflect.Method;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Set;

public class Reflections {

    private final Set<Class<?>> WRAPPER_TYPES = getWrapperTypes();

    public boolean isWrapperType(Class<?> clazz)
    {
        return WRAPPER_TYPES.contains(clazz);
    }

    private Set<Class<?>> getWrapperTypes()
    {
        Set<Class<?>> ret = new HashSet<Class<?>>();
        ret.add(Boolean.class);
        ret.add(Character.class);
        ret.add(Byte.class);
        ret.add(Short.class);
        ret.add(Integer.class);
        ret.add(Long.class);
        ret.add(Float.class);
        ret.add(Double.class);
        ret.add(Void.class);
        return ret;
    }

    public static void main (String[] args) throws Exception {
        HashMap<String, Object> m = new HashMap<>();
        m = new Reflections().go(m, SimpleInterface.class);
        System.out.println(new GsonBuilder().setPrettyPrinting().create().toJson(m));
    }
    public HashMap<String, Object> go(HashMap<String, Object> map, Class<?> c) {
        for (Method m: c.getMethods()) {
            if (!isWrapperType(m.getReturnType())) {
                HashMap<String, Object> newMap = new HashMap<>();
                newMap = go(newMap, m.getReturnType());
                map.put(m.getName(), newMap);

            } else {
                map.put(m.getName(), m.getReturnType().getSimpleName());
            }
        }
        return map;
    }
}
