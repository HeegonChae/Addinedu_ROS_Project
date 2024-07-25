// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from task_manager:msg/GuiUpdate.idl
// generated code does not contain a copyright notice
#include "task_manager/msg/detail/gui_update__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `product_code`
// Member `status`
// Member `message`
#include "rosidl_runtime_c/string_functions.h"

bool
task_manager__msg__GuiUpdate__init(task_manager__msg__GuiUpdate * msg)
{
  if (!msg) {
    return false;
  }
  // product_code
  if (!rosidl_runtime_c__String__init(&msg->product_code)) {
    task_manager__msg__GuiUpdate__fini(msg);
    return false;
  }
  // status
  if (!rosidl_runtime_c__String__init(&msg->status)) {
    task_manager__msg__GuiUpdate__fini(msg);
    return false;
  }
  // message
  if (!rosidl_runtime_c__String__init(&msg->message)) {
    task_manager__msg__GuiUpdate__fini(msg);
    return false;
  }
  return true;
}

void
task_manager__msg__GuiUpdate__fini(task_manager__msg__GuiUpdate * msg)
{
  if (!msg) {
    return;
  }
  // product_code
  rosidl_runtime_c__String__fini(&msg->product_code);
  // status
  rosidl_runtime_c__String__fini(&msg->status);
  // message
  rosidl_runtime_c__String__fini(&msg->message);
}

bool
task_manager__msg__GuiUpdate__are_equal(const task_manager__msg__GuiUpdate * lhs, const task_manager__msg__GuiUpdate * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // product_code
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->product_code), &(rhs->product_code)))
  {
    return false;
  }
  // status
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->status), &(rhs->status)))
  {
    return false;
  }
  // message
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->message), &(rhs->message)))
  {
    return false;
  }
  return true;
}

bool
task_manager__msg__GuiUpdate__copy(
  const task_manager__msg__GuiUpdate * input,
  task_manager__msg__GuiUpdate * output)
{
  if (!input || !output) {
    return false;
  }
  // product_code
  if (!rosidl_runtime_c__String__copy(
      &(input->product_code), &(output->product_code)))
  {
    return false;
  }
  // status
  if (!rosidl_runtime_c__String__copy(
      &(input->status), &(output->status)))
  {
    return false;
  }
  // message
  if (!rosidl_runtime_c__String__copy(
      &(input->message), &(output->message)))
  {
    return false;
  }
  return true;
}

task_manager__msg__GuiUpdate *
task_manager__msg__GuiUpdate__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  task_manager__msg__GuiUpdate * msg = (task_manager__msg__GuiUpdate *)allocator.allocate(sizeof(task_manager__msg__GuiUpdate), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(task_manager__msg__GuiUpdate));
  bool success = task_manager__msg__GuiUpdate__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
task_manager__msg__GuiUpdate__destroy(task_manager__msg__GuiUpdate * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    task_manager__msg__GuiUpdate__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
task_manager__msg__GuiUpdate__Sequence__init(task_manager__msg__GuiUpdate__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  task_manager__msg__GuiUpdate * data = NULL;

  if (size) {
    data = (task_manager__msg__GuiUpdate *)allocator.zero_allocate(size, sizeof(task_manager__msg__GuiUpdate), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = task_manager__msg__GuiUpdate__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        task_manager__msg__GuiUpdate__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
task_manager__msg__GuiUpdate__Sequence__fini(task_manager__msg__GuiUpdate__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      task_manager__msg__GuiUpdate__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

task_manager__msg__GuiUpdate__Sequence *
task_manager__msg__GuiUpdate__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  task_manager__msg__GuiUpdate__Sequence * array = (task_manager__msg__GuiUpdate__Sequence *)allocator.allocate(sizeof(task_manager__msg__GuiUpdate__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = task_manager__msg__GuiUpdate__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
task_manager__msg__GuiUpdate__Sequence__destroy(task_manager__msg__GuiUpdate__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    task_manager__msg__GuiUpdate__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
task_manager__msg__GuiUpdate__Sequence__are_equal(const task_manager__msg__GuiUpdate__Sequence * lhs, const task_manager__msg__GuiUpdate__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!task_manager__msg__GuiUpdate__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
task_manager__msg__GuiUpdate__Sequence__copy(
  const task_manager__msg__GuiUpdate__Sequence * input,
  task_manager__msg__GuiUpdate__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(task_manager__msg__GuiUpdate);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    task_manager__msg__GuiUpdate * data =
      (task_manager__msg__GuiUpdate *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!task_manager__msg__GuiUpdate__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          task_manager__msg__GuiUpdate__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!task_manager__msg__GuiUpdate__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
