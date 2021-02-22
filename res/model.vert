#version 330

layout (location = 0) in vec3 vertex_position;
layout (location = 1) in vec3 vertex_normal;
layout (location = 2) in vec3 vertex_colour;

uniform mat4   model;
uniform mat4   view;
uniform mat4   projection;

uniform vec3 lightPos;

out vec3 frag_normal;
out vec3 frag_pos;
out vec3 frag_colour;
out vec3 frag_lightPos;

void main()
{
    gl_Position = projection * view * model * vec4(vertex_position, 1.0);
    frag_pos = vec3(view * model * vec4(vertex_position, 1.0f));
    frag_normal = mat3(transpose(inverse(view * model))) * vertex_normal;
    frag_colour = vertex_colour;
    frag_lightPos = vec3(view * vec4(lightPos, 1.0));
}